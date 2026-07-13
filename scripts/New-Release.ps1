$ErrorActionPreference = 'Stop'

$root = Split-Path -Parent $PSScriptRoot
$manifest = Get-Content -Raw (Join-Path $root 'kit-manifest.json') | ConvertFrom-Json
$dist = Join-Path $root 'dist'

if (Test-Path $dist) { Remove-Item -LiteralPath $dist -Recurse -Force }
New-Item -ItemType Directory -Path $dist | Out-Null

foreach ($package in $manifest.packages) {
  $source = Join-Path $root (Join-Path 'packages' $package.id)
  $archive = Join-Path $dist $package.archive
  Compress-Archive -Path (Join-Path $source '*') -DestinationPath $archive -CompressionLevel Optimal
  $hash = (Get-FileHash -Algorithm SHA256 -LiteralPath $archive).Hash.ToLowerInvariant()
  Set-Content -NoNewline -Encoding ascii -Path "$archive.sha256" -Value "$hash  $($package.archive)"
  Write-Host "Created $($package.archive)"
}

Copy-Item -LiteralPath (Join-Path $root 'kit-manifest.json') -Destination (Join-Path $dist 'kit-manifest.json')
