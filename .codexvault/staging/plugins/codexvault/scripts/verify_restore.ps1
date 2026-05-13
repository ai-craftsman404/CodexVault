param(
    [Parameter(Mandatory=$true)][string]$PlanJson
)

. "$PSScriptRoot/lib/codexvault-shared.ps1"

$planEnvelope = $PlanJson | ConvertFrom-Json
if ($planEnvelope.PSObject.Properties.Name -contains 'plan') {
    $plan = $planEnvelope.plan
    $planPath = $planEnvelope.planPath
} else {
    $plan = $planEnvelope
    $planPath = $null
}

$reasons = @()
if (-not $plan.approvalRequired) {
    $reasons += 'restore plan did not require approval'
}
if (-not $plan.checkpoints -or $plan.checkpoints.Count -eq 0) {
    $reasons += 'restore plan missing checkpoints'
}

$validationStatus = if ($reasons.Count -eq 0) { 'validated' } else { 'validated-with-warnings' }
if ($reasons.Count -gt 1) {
    $validationStatus = 'not-validated'
}

$report = [pscustomobject]@{
    schemaVersion = 'v1a'
    validationStatus = $validationStatus
    summary = if ($validationStatus -eq 'validated') { 'Restore verified' } elseif ($validationStatus -eq 'validated-with-warnings') { 'Restore verified with warnings' } else { 'Restore not validated' }
    reasons = $reasons
}

$workspacePath = if ($planPath) { Split-Path -Parent (Split-Path -Parent $planPath) } else { (Get-Location).Path }
$paths = Get-CvxPathConfig -WorkspacePath $workspacePath
if (-not (Test-Path -LiteralPath $paths.verificationDir)) {
    New-Item -ItemType Directory -Path $paths.verificationDir -Force | Out-Null
}
$verificationPath = Join-Path $paths.verificationDir "verification-$((Get-Date).ToString('yyyyMMddTHHmmssZ')).json"
($report | ConvertTo-Json -Depth 6) | Set-Content -LiteralPath $verificationPath -Encoding UTF8

[pscustomobject]@{
    verificationPath = $verificationPath
    report = $report
} | ConvertTo-Json -Depth 6
