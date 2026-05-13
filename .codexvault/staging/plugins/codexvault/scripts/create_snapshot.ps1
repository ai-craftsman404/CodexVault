param(
    [Parameter(Mandatory=$true)][string]$ManifestJson,
    [string]$OutputDirectory = (Join-Path (Get-Location).Path '.codexvault')
)

. "$PSScriptRoot/lib/codexvault-shared.ps1"

$manifest = $ManifestJson | ConvertFrom-Json
$manifestText = ($ManifestJson.Trim())
$archiveName = "codexvault-$($manifest.workspaceId)-$(New-CvxTimestamp)-$($manifest.platform).zip"
$outDir = if (Test-Path -LiteralPath $OutputDirectory) {
    (Resolve-Path -LiteralPath $OutputDirectory).Path
} else {
    [IO.Path]::GetFullPath($OutputDirectory)
}
if (-not (Test-Path -LiteralPath $outDir)) {
    New-Item -ItemType Directory -Path $outDir | Out-Null
}

$stagingDir = Join-Path $outDir 'staging'
if (Test-Path -LiteralPath $stagingDir) {
    Remove-Item -LiteralPath $stagingDir -Recurse -Force
}
New-Item -ItemType Directory -Path $stagingDir | Out-Null

$workspacePath = $manifest.workspacePath
if (-not $workspacePath) { throw 'Manifest missing workspacePath' }
$files = Get-CvxWorkspaceFiles -WorkspacePath $workspacePath
foreach ($file in $files) {
    $relative = $file.FullName.Substring($workspacePath.Length).TrimStart('\','/')
    $target = Join-Path $stagingDir $relative
    $targetDir = Split-Path -Parent $target
    if (-not (Test-Path -LiteralPath $targetDir)) {
        New-Item -ItemType Directory -Path $targetDir -Force | Out-Null
    }
    Copy-Item -LiteralPath $file.FullName -Destination $target -Force
}

if (-not (Get-ChildItem -LiteralPath $stagingDir -Recurse -File -ErrorAction SilentlyContinue)) {
    Set-Content -LiteralPath (Join-Path $stagingDir '.cvx-placeholder') -Value 'CodexVault snapshot placeholder' -Encoding UTF8
}

$archivePath = Join-Path $outDir $archiveName
if (Test-Path -LiteralPath $archivePath) {
    Remove-Item -LiteralPath $archivePath -Force
}
Compress-Archive -Path (Join-Path $stagingDir '*') -DestinationPath $archivePath -Force
$checksum = New-CvxSha256File -Path $archivePath
$sidecar = [pscustomobject]@{
    archivePath = $archiveName
    checksumAlgorithm = 'SHA-256'
    checksum = $checksum
}
($sidecar | ConvertTo-Json -Depth 4) | Set-Content -LiteralPath (Join-Path $outDir ($archiveName + '.sha256.json')) -Encoding UTF8

$snapshot = [pscustomobject]@{
    schemaVersion = $manifest.schemaVersion
    workspaceId = $manifest.workspaceId
    createdAt = New-CvxTimestamp
    archivePath = $archivePath
    checksum = $checksum
    checksumAlgorithm = 'SHA-256'
    status = 'snapshot complete'
}

$snapshot | ConvertTo-Json -Depth 6
