import { readFile, readdir, stat } from 'node:fs/promises';
import { dirname, resolve, relative, sep } from 'node:path';

const root = resolve(import.meta.dirname, '..');
const manifest = JSON.parse(await readFile(resolve(root, 'kit-manifest.json'), 'utf8'));
const requiredGuardrails = ['humanApproval', 'clientData', 'aiRole', 'prohibited'];
const failures = [];
const pluginRoot = resolve(root, 'plugins', 'ana-hr-operations');

async function findMarkdownFiles(directory) {
  const files = [];
  for (const entry of await readdir(directory, { withFileTypes: true })) {
    if (entry.name === '.git' || entry.name === 'node_modules') continue;
    const entryPath = resolve(directory, entry.name);
    if (entry.isDirectory()) files.push(...await findMarkdownFiles(entryPath));
    else if (entry.isFile() && entry.name.toLowerCase().endsWith('.md')) files.push(entryPath);
  }
  return files;
}

if (manifest.schema !== 'ana-ai-business-kit/v1') failures.push('Unexpected manifest schema.');
if (manifest.version !== '1.1.0') failures.push('Kit manifest must be version 1.1.0.');
if (manifest.packages?.length !== 2) failures.push('Exactly two downloads are required.');
for (const key of requiredGuardrails) if (!(key in manifest.guardrails)) failures.push(`Missing guardrail: ${key}`);

for (const pkg of manifest.packages ?? []) {
  if (!pkg.id || !pkg.archive || !pkg.entrypoint || !Array.isArray(pkg.files)) {
    failures.push(`Invalid package manifest entry: ${pkg.id ?? 'unknown'}.`);
    continue;
  }
  if (!pkg.archive.endsWith(`-v${manifest.version}.zip`)) {
    failures.push(`Package archive version must match kit ${manifest.version}: ${pkg.archive}`);
  }
  for (const file of pkg.files) {
    const destination = resolve(root, 'packages', pkg.id, file);
    if (!destination.startsWith(resolve(root, 'packages', pkg.id) + sep)) {
      failures.push(`Unsafe file path: ${pkg.id}/${file}`);
      continue;
    }
    try {
      await stat(destination);
    } catch {
      failures.push(`Missing package file: ${relative(root, destination)}`);
    }
  }
}

const operatorInstructions = await readFile(resolve(root, 'packages/ana-operator-kit/AGENTS.md'), 'utf8');
for (const required of ['PRACTITIONER REVIEW REQUIRED', 'Never diagnose', 'private']) {
  if (!operatorInstructions.toLowerCase().includes(required.toLowerCase())) failures.push(`Operator guardrail missing: ${required}`);
}

const pluginManifest = JSON.parse(await readFile(resolve(pluginRoot, '.codex-plugin', 'plugin.json'), 'utf8'));
if (pluginManifest.name !== 'ana-hr-operations') failures.push('Plugin name must match its folder.');
if (!/^0\.2\.0(?:\+codex\.[0-9A-Za-z.-]+)?$/.test(pluginManifest.version)) failures.push('Plugin version must preserve the 0.2.0 base version and optional Codex cachebuster.');
if (!pluginManifest.skills) failures.push('Plugin skills path is required.');

const marketplace = JSON.parse(await readFile(resolve(root, '.agents', 'plugins', 'marketplace.json'), 'utf8'));
if (marketplace.name !== 'ana-business-kit') failures.push('Marketplace name must be ana-business-kit.');
const marketplacePlugin = marketplace.plugins?.find((plugin) => plugin.name === 'ana-hr-operations');
if (!marketplacePlugin) failures.push('Marketplace entry for ana-hr-operations is missing.');
if (marketplacePlugin?.source?.path !== './plugins/ana-hr-operations') failures.push('Marketplace plugin path is invalid.');

for (const guide of [
  'README.md',
  'START-HERE-ANA.md',
  'START-HERE-TEAM.md',
  'docs/FORK-AND-INSTALL-CODEX.md',
  'docs/GOOGLE-DOCS-SETUP.md',
  'docs/FIRST-CLIENT-FLOW.md',
  'docs/TEAM-ADOPTION.md',
  'docs/GOOGLE-WORKSPACE-AND-TEMPLATES.md',
  'docs/TEMPLATE-AND-CANVA-ROUTING.md',
  'docs/PRACTICE-ENGAGEMENT.md',
  'docs/TEAM-STARTER-PROMPTS.md',
  'docs/RELEASE-AND-UPDATE.md',
  'docs/HR-AGENCY-ADAPTATION.md',
  'docs/WHO-READS-WHAT.md',
  'docs/TEMPLATE-STUDIO-V1.2.md',
]) {
  try {
    const guideText = await readFile(resolve(root, guide), 'utf8');
    if (!guideText.trim()) failures.push(`Empty guide: ${guide}`);
  } catch {
    failures.push(`Missing guide: ${guide}`);
  }
}

for (const markdownFile of await findMarkdownFiles(root)) {
  const markdown = await readFile(markdownFile, 'utf8');
  for (const match of markdown.matchAll(/!?\[[^\]]*\]\(([^)]+)\)/g)) {
    let target = match[1].trim();
    if (target.startsWith('<') && target.endsWith('>')) target = target.slice(1, -1);
    if (/^(?:https?:|mailto:|tel:|#)/i.test(target)) continue;
    target = target.split('#', 1)[0].split('?', 1)[0];
    if (!target) continue;
    try {
      target = decodeURIComponent(target);
    } catch {
      failures.push(`Invalid link encoding in ${relative(root, markdownFile)}: ${match[1]}`);
      continue;
    }
    const destination = resolve(dirname(markdownFile), target);
    if (destination !== root && !destination.startsWith(root + sep)) {
      failures.push(`Local link leaves the repository in ${relative(root, markdownFile)}: ${match[1]}`);
      continue;
    }
    try {
      await stat(destination);
    } catch {
      failures.push(`Broken local link in ${relative(root, markdownFile)}: ${match[1]}`);
    }
  }
}

const rootReadme = await readFile(resolve(root, 'README.md'), 'utf8');
for (const required of [
  'codex plugin marketplace add frankxai/ana-ai-business-kit --ref main',
  'codex plugin add ana-hr-operations@ana-business-kit',
  'first call',
  'Google Docs',
]) {
  if (!rootReadme.toLowerCase().includes(required.toLowerCase())) failures.push(`README onboarding content missing: ${required}`);
}

const publicEntries = [
  'README.md',
  'START-HERE-ANA.md',
  'START-HERE-TEAM.md',
  'FOUNDATION.md',
  'docs/TEAM-ADOPTION.md',
  'docs/WHO-READS-WHAT.md',
  'plugins/ana-hr-operations/.codex-plugin/plugin.json',
  'plugins/ana-hr-operations/skills/ana-hr-operations/agents/openai.yaml',
];

const publicEntryContents = await Promise.all(
  publicEntries.map(async (entry) => ({
    entry,
    content: (await readFile(resolve(root, entry), 'utf8')).toLowerCase(),
  })),
);

const staleFramings = [
  'four-person adoption product',
  'this is your four-person hr operating kit',
  'the simple model',
  'the point is not to make the team technical',
  'your first 20 minutes',
  'first 45 minutes',
  'one rule to remember',
  'the team is ready for normal use when it can demonstrate',
  'asking all four people to work directly in github',
];

for (const { entry, content } of publicEntryContents) {
  for (const staleFraming of staleFramings) {
    if (content.includes(staleFraming)) failures.push(`${entry} contains stale onboarding framing: ${staleFraming}`);
  }
}

const skillRoot = resolve(pluginRoot, 'skills', 'ana-hr-operations');
const skillText = await readFile(resolve(skillRoot, 'SKILL.md'), 'utf8');
if (skillText.includes('[TODO:')) failures.push('Skill contains TODO placeholders.');
for (const relativePath of [
  'agents/openai.yaml',
  'scripts/validate_engagement.py',
  'scripts/render_documents.py',
  'scripts/test_engagement.py',
  'scripts/test_sops.py',
  'assets/client-kickoff.md',
  'assets/job-description.md',
  'assets/offer.md',
  'assets/invoice.md',
  'assets/engagement.example.json',
  'assets/daily-operations-board.md',
  'assets/recruiting-weekly-status.md',
  'assets/template-registry.example.json',
  'assets/team-workspace.example.json',
  'references/sop-index.md',
  'references/workflow.md',
  'references/record-contract.md',
  'references/google-docs-template.md',
  'references/hr-quality-and-privacy.md',
  'references/pricing-and-invoice.md',
  'references/team-adoption-and-template-ops.md',
  'references/sops/SOP-00-multi-client-control.md',
  'references/sops/SOP-01-first-client-call.md',
  'references/sops/SOP-02-client-kickoff.md',
  'references/sops/SOP-03-job-description.md',
  'references/sops/SOP-04-offer-and-pricing.md',
  'references/sops/SOP-05-recruiting-delivery.md',
  'references/sops/SOP-06-invoice.md',
  'references/sops/SOP-07-send-and-handoff.md',
]) {
  try {
    await stat(resolve(skillRoot, relativePath));
  } catch {
    failures.push(`Missing plugin resource: ${relativePath}`);
  }
}

for (const [skillName, resources] of Object.entries({
  'ana-research-library': [
    'SKILL.md',
    'agents/openai.yaml',
    'references/research-standard.md',
    'references/source-seed-list.md',
    'assets/research-entry.example.json',
    'scripts/validate_research_entry.py',
    'scripts/test_research_library.py',
  ],
  'ana-approved-content': [
    'SKILL.md',
    'agents/openai.yaml',
    'references/editorial-safety.md',
    'assets/content-brief.example.json',
    'scripts/validate_content_brief.py',
    'scripts/test_approved_content.py',
  ],
  'ana-template-studio': [
    'SKILL.md',
    'agents/openai.yaml',
    'references/template-job-contract.md',
    'references/docs-canva-runbook.md',
    'references/specialist-orchestration.md',
    'assets/template-job.example.json',
    'scripts/validate_template_job.py',
    'scripts/test_template_studio.py',
  ],
})) {
  const specialSkillRoot = resolve(pluginRoot, 'skills', skillName);
  for (const relativePath of resources) {
    try {
      await stat(resolve(specialSkillRoot, relativePath));
    } catch {
      failures.push(`Missing ${skillName} resource: ${relativePath}`);
    }
  }
}

if (failures.length) {
  console.error('Kit validation failed:');
  for (const failure of failures) console.error(`- ${failure}`);
  process.exit(1);
}

console.log(`Validated ${manifest.packages.length} downloads, ${manifest.packages.reduce((count, pkg) => count + pkg.files.length, 0)} package files, and the Ana HR Operations plugin.`);
