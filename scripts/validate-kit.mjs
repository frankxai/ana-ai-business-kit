import { readFile, stat } from 'node:fs/promises';
import { resolve, relative, sep } from 'node:path';

const root = resolve(import.meta.dirname, '..');
const manifest = JSON.parse(await readFile(resolve(root, 'kit-manifest.json'), 'utf8'));
const requiredGuardrails = ['humanApproval', 'clientData', 'aiRole', 'prohibited'];
const failures = [];

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

if (failures.length) {
  console.error('Kit validation failed:');
  for (const failure of failures) console.error(`- ${failure}`);
  process.exit(1);
}

console.log(`Validated ${manifest.packages.length} downloads and ${manifest.packages.reduce((count, pkg) => count + pkg.files.length, 0)} package files.`);
