param(
    [Parameter(Mandatory=$true)][string]$DiscoveryJson
)

. "$PSScriptRoot/lib/codexvault-shared.ps1"

$discovery = $DiscoveryJson | ConvertFrom-Json
$paths = Get-CvxPathConfig -WorkspacePath $discovery.workspacePath
$manifestDir = $paths.manifestOutputDir
if (-not (Test-Path -LiteralPath $manifestDir)) {
    New-Item -ItemType Directory -Path $manifestDir -Force | Out-Null
}
$seed = "$($discovery.workspacePath)|$($discovery.os)|$($discovery.shell)|$($discovery.timestamp)"
$manifest = [pscustomobject]@{
    schemaVersion = 'v1a'
    workspaceId = (New-CvxStableGuid -Seed $seed).ToString()
    capturedAt = New-CvxTimestamp
    platform = $discovery.os
    shell = $discovery.shell
    workspacePath = $discovery.workspacePath
    codexEnv = [ordered]@{}
    gitState = [ordered]@{}
    toolchainState = [ordered]@{}
    fileInventorySummary = [ordered]@{}
    integrity = [ordered]@{}
    redactionPolicy = 'deny-by-default'
}

$manifestJson = $manifest | ConvertTo-Json -Depth 8
$manifestPath = Join-Path $manifestDir "manifest-$($manifest.workspaceId).json"
$manifestJson | Set-Content -LiteralPath $manifestPath -Encoding UTF8

[pscustomobject]@{
    manifestPath = $manifestPath
    manifest = $manifest
} | ConvertTo-Json -Depth 8
