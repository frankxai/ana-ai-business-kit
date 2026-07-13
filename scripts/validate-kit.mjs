import { readFile, stat } from 'node:fs/promises';
import { resolve, relative, sep } from 'node:path';

const root = resolve(import.meta.dirname, '..');
const manifest = JSON.parse(await readFile(resolve(root, 'kit-manifest.json'), 'utf8'));
const requiredGuardrails = ['humanApproval', 'clientData', 'aiRole', 'prohibited'];
const failures = [];
const pluginRoot = resolve(root, 'plugins', 'ana-hr-operations');

if (manifest.schema !== 'ana-ai-business-kit/v1') failures.push('Unexpected manifest schema.');
if (manifest.packages?.length !== 2) failures.push('Exactly two downloads are required.');
for (const key of requiredGuardrails) if (!(key in manifest.guardrails)) failures.push(`Missing guardrail: ${key}`);

for (const pkg of manifest.packages ?? []) {
  if (!pkg.id || !pkg.archive || !pkg.entrypoint || !Array.isArray(pkg.files)) {
    failures.push(`Invalid package manifest entry: ${pkg.id ?? 'unknown'}.`);
    continue;
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
if (pluginManifest.version !== '0.1.0') failures.push('Plugin version must be 0.1.0.');
if (!pluginManifest.skills) failures.push('Plugin skills path is required.');

const marketplace = JSON.parse(await readFile(resolve(root, '.agents', 'plugins', 'marketplace.json'), 'utf8'));
if (marketplace.name !== 'ana-business-kit') failures.push('Marketplace name must be ana-business-kit.');
const marketplacePlugin = marketplace.plugins?.find((plugin) => plugin.name === 'ana-hr-operations');
if (!marketplacePlugin) failures.push('Marketplace entry for ana-hr-operations is missing.');
if (marketplacePlugin?.source?.path !== './plugins/ana-hr-operations') failures.push('Marketplace plugin path is invalid.');

for (const guide of [
  'README.md',
  'START-HERE-ANA.md',
  'docs/FORK-AND-INSTALL-CODEX.md',
  'docs/GOOGLE-DOCS-SETUP.md',
  'docs/FIRST-CLIENT-FLOW.md',
]) {
  try {
    const guideText = await readFile(resolve(root, guide), 'utf8');
    if (!guideText.trim()) failures.push(`Empty guide: ${guide}`);
  } catch {
    failures.push(`Missing guide: ${guide}`);
  }
}

const rootReadme = await readFile(resolve(root, 'README.md'), 'utf8');
for (const required of [
  'codex plugin marketplace add frankxai/ana-ai-business-kit --ref main',
  'codex plugin add ana-hr-operations@ana-business-kit',
  'first client call',
  'Google Docs',
]) {
  if (!rootReadme.toLowerCase().includes(required.toLowerCase())) failures.push(`README onboarding content missing: ${required}`);
}

const skillRoot = resolve(pluginRoot, 'skills', 'ana-hr-operations');
const skillText = await readFile(resolve(skillRoot, 'SKILL.md'), 'utf8');
if (skillText.includes('[TODO:')) failures.push('Skill contains TODO placeholders.');
for (const relativePath of [
  'agents/openai.yaml',
  'scripts/validate_engagement.py',
  'scripts/render_documents.py',
  'scripts/test_engagement.py',
  'assets/client-kickoff.md',
  'assets/job-description.md',
  'assets/offer.md',
  'assets/invoice.md',
  'assets/engagement.example.json',
  'references/workflow.md',
  'references/record-contract.md',
  'references/google-docs-template.md',
  'references/hr-quality-and-privacy.md',
  'references/pricing-and-invoice.md',
]) {
  try {
    await stat(resolve(skillRoot, relativePath));
  } catch {
    failures.push(`Missing plugin resource: ${relativePath}`);
  }
}

if (failures.length) {
  console.error('Kit validation failed:');
  for (const failure of failures) console.error(`- ${failure}`);
  process.exit(1);
}

console.log(`Validated ${manifest.packages.length} downloads, ${manifest.packages.reduce((count, pkg) => count + pkg.files.length, 0)} package files, and the Ana HR Operations plugin.`);
