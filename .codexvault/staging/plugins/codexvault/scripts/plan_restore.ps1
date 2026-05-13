param(
    [Parameter(Mandatory=$true)][string]$ManifestJson
)

. "$PSScriptRoot/lib/codexvault-shared.ps1"

$plan = [pscustomobject]@{
    schemaVersion = 'v1a'
    status = 'restore plan ready'
    checkpoints = @(
        'validate archive',
        'prepare isolated temp dir',
        'request approval for in-place changes'
    )
    approvalRequired = $true
    tempRestoreScope = 'plugin-managed isolated temp-dir only'
}

$manifest = $ManifestJson | ConvertFrom-Json
$paths = Get-CvxPathConfig -WorkspacePath $manifest.workspacePath
if (-not (Test-Path -LiteralPath $paths.restorePlanDir)) {
    New-Item -ItemType Directory -Path $paths.restorePlanDir -Force | Out-Null
}
$planPath = Join-Path $paths.restorePlanDir "restore-plan-$($manifest.workspaceId).json"
$planJson = $plan | ConvertTo-Json -Depth 6
$planJson | Set-Content -LiteralPath $planPath -Encoding UTF8

[pscustomobject]@{
    planPath = $planPath
    plan = $plan
} | ConvertTo-Json -Depth 6
