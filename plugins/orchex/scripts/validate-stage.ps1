[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$RunPath,

    [Parameter(Mandatory = $true)]
    [ValidateSet("start", "plan", "build", "test", "review")]
    [string]$CurrentStage,

    [Parameter(Mandatory = $true)]
    [ValidateSet("plan", "build", "test", "review", "done")]
    [string]$TargetStage,

    [switch]$RequireApproval
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$allowedTransitions = @{
    start  = @("plan")
    plan   = @("build")
    build  = @("test")
    test   = @("review")
    review = @("done")
}

function Fail-Validation {
    param([string]$Reason)
    [pscustomobject]@{
        ok          = $false
        currentStage = $CurrentStage
        targetStage = $TargetStage
        reason      = $Reason
    } | ConvertTo-Json -Depth 4
    exit 1
}

if (-not $allowedTransitions.ContainsKey($CurrentStage) -or ($allowedTransitions[$CurrentStage] -notcontains $TargetStage)) {
    Fail-Validation "Unsupported stage transition: $CurrentStage -> $TargetStage"
}

$scriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$artifactStage = switch ($TargetStage) {
    "plan" { $null }
    "build" { "plan" }
    "test" { "build" }
    "review" { "test" }
    "done" { "review" }
}

if ($artifactStage) {
    try {
        & (Join-Path $scriptRoot "validate-artifacts.ps1") -RunPath $RunPath -Stage $artifactStage | Out-Null
    }
    catch {
        Fail-Validation "Required artifacts for stage '$artifactStage' are missing."
    }
}

try {
    $ownershipValidation = & (Join-Path $scriptRoot "validate-ownership.ps1") -RunPath $RunPath
    $ownershipResult = $ownershipValidation | ConvertFrom-Json
    if (-not $ownershipResult.ok) {
        Fail-Validation "Ownership validation failed."
    }
}
catch {
    Fail-Validation "Ownership validation failed."
}

$resolvedRunPath = (Resolve-Path -LiteralPath $RunPath).Path
$metadataPath = Join-Path $resolvedRunPath "run-metadata.json"
$metadata = Get-Content -LiteralPath $metadataPath -Raw | ConvertFrom-Json
$runId = [string]$metadata.runId
$taskLedgerPath = Join-Path $resolvedRunPath "task-ledger.md"

if (Test-Path -LiteralPath $taskLedgerPath) {
    $taskLedger = Get-Content -LiteralPath $taskLedgerPath -Raw
    if ($taskLedger -match "(?im)^\s*Current Stage:\s*(\S+)") {
        $recordedStage = $matches[1]
        if ($CurrentStage -ne "start" -and $recordedStage -ne $CurrentStage) {
            Fail-Validation "Task ledger current stage '$recordedStage' does not match requested current stage '$CurrentStage'."
        }
    }
}

if ($TargetStage -eq "review" -or $TargetStage -eq "done") {
    $testReportPath = Join-Path $resolvedRunPath "test-report.md"
    $testReport = Get-Content -LiteralPath $testReportPath -Raw
    if ($testReport -notmatch ("(?im)^\s*Run ID:\s*" + [regex]::Escape($runId) + "\s*$")) {
        Fail-Validation "Test report run ID does not match run metadata."
    }
    if ($testReport -notmatch "RESULT:\s*PASS") {
        Fail-Validation "Test report does not show a passing result."
    }

    if ($testReport -notmatch "EVIDENCE:\s*\S+") {
        Fail-Validation "Test report is missing execution evidence."
    }
}

if ($TargetStage -eq "done" -and $RequireApproval) {
    $approvalPath = Join-Path $resolvedRunPath "approval-note.md"
    if (-not (Test-Path -LiteralPath $approvalPath)) {
        Fail-Validation "Approval is required before completion, but approval-note.md is missing."
    }

    $approvalNote = Get-Content -LiteralPath $approvalPath -Raw
    if ($approvalNote -notmatch ("(?im)^\s*Run ID:\s*" + [regex]::Escape($runId) + "\s*$")) {
        Fail-Validation "Approval note run ID does not match run metadata."
    }
}

[pscustomobject]@{
    ok           = $true
    currentStage = $CurrentStage
    targetStage  = $TargetStage
    reason       = "Validation passed."
} | ConvertTo-Json -Depth 4
