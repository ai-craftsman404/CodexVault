[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$RunRecordPath,

    [Parameter(Mandatory = $true)]
    [string]$StepId,

    [Parameter(Mandatory = $true)]
    [ValidateSet("pass", "fail", "blocked", "not-run")]
    [string]$Status,

    [string]$Note,

    [string]$EvidenceItem,

    [string]$Issue,

    [string]$RecommendedFix,

    [string]$SmokeTestPrompt,

    [string]$SmokeTestExpectedBehavior,

    [string]$SmokeTestObservedBehavior
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

if (-not (Test-Path -LiteralPath $RunRecordPath)) {
    throw "Run record not found: $RunRecordPath"
}

$runDir = Split-Path -Parent $RunRecordPath
$record = Get-Content -LiteralPath $RunRecordPath -Raw | ConvertFrom-Json
$step = $record.steps | Where-Object { $_.id -eq $StepId } | Select-Object -First 1

if ($null -eq $step) {
    throw "Unknown StepId: $StepId"
}

$step.status = $Status
if ($PSBoundParameters.ContainsKey("Note") -and -not [string]::IsNullOrWhiteSpace($Note)) {
    $step.notes = @($step.notes) + $Note
}
if ($PSBoundParameters.ContainsKey("EvidenceItem") -and -not [string]::IsNullOrWhiteSpace($EvidenceItem)) {
    $step.evidence = @($step.evidence) + $EvidenceItem
}
if ($PSBoundParameters.ContainsKey("Issue") -and -not [string]::IsNullOrWhiteSpace($Issue)) {
    $record.issues = @($record.issues) + $Issue
}
if ($PSBoundParameters.ContainsKey("RecommendedFix") -and -not [string]::IsNullOrWhiteSpace($RecommendedFix)) {
    $record.recommendedFixes = @($record.recommendedFixes) + $RecommendedFix
}

if ($StepId -eq "smoke-test") {
    if ($PSBoundParameters.ContainsKey("SmokeTestPrompt")) {
        $record.smokeTest.prompt = $SmokeTestPrompt
    }
    if ($PSBoundParameters.ContainsKey("SmokeTestExpectedBehavior")) {
        $record.smokeTest.expectedBehavior = $SmokeTestExpectedBehavior
    }
    if ($PSBoundParameters.ContainsKey("SmokeTestObservedBehavior")) {
        $record.smokeTest.observedBehavior = $SmokeTestObservedBehavior
    }
}

$stepStatuses = @($record.steps | ForEach-Object { $_.status })
if ($stepStatuses -contains "fail") {
    $record.overallResult = "fail"
    $record.status = "completed"
}
elseif ($stepStatuses -contains "blocked") {
    $record.overallResult = "blocked"
    $record.status = "completed"
}
elseif ($stepStatuses -notcontains "not-run") {
    $record.overallResult = "pass"
    $record.status = "completed"
}
else {
    $record.overallResult = "in-progress"
    $record.status = "running"
}

$record.updatedAt = (Get-Date).ToUniversalTime().ToString("o")
$record | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $RunRecordPath

$rows = foreach ($item in $record.steps) {
    $itemNotes = @($item.notes | Where-Object { $null -ne $_ -and $_ -ne "" })
    $notesText = if (@($itemNotes).Count -gt 0) { ($itemNotes -join "; ") } else { "" }
    "| $($item.label) | $($item.status) | $notesText |"
}

@(
    "# Codex Last-Mile Verification Checklist"
    ""
    "- Run ID: $($record.runId)"
    "- Updated: $($record.updatedAt)"
    "- Target: $($record.target.name) ($($record.target.type))"
    "- Overall result: $($record.overallResult)"
    ""
    "## Preflight"
    ""
    "- Local path exists: $($record.preflight.localPathExists)"
    "- Expected entrypoint exists: $($record.preflight.entrypointExists)"
    ""
    "## Live Steps"
    ""
    "| Step | Status | Notes |"
    "| --- | --- | --- |"
) + $rows | Set-Content -LiteralPath (Join-Path $runDir "checklist.md")

$issueItems = @($record.issues | Where-Object { $null -ne $_ -and $_ -ne "" })
$issueLines = if (@($issueItems).Count -gt 0) {
    $issueItems | ForEach-Object { "- $_" }
} else {
    @("- No issues recorded yet.")
}

$fixItems = @($record.recommendedFixes | Where-Object { $null -ne $_ -and $_ -ne "" })
$fixLines = if (@($fixItems).Count -gt 0) {
    $fixItems | ForEach-Object { "- $_" }
} else {
    @("- No recommended fixes recorded yet.")
}

@(
    "# Final Verification Summary"
    ""
    "- Run ID: $($record.runId)"
    "- Updated: $($record.updatedAt)"
    "- Overall result: $($record.overallResult)"
    ""
    "## Outcome"
    ""
    "- Target: $($record.target.name) ($($record.target.type))"
    "- Invocation method: $($record.target.expectedInvocationMethod)"
    ""
    "## Step Results"
    ""
) + $rows + @(
    ""
    "## Issues Found"
    ""
) + $issueLines + @(
    ""
    "## Recommended Fixes"
    ""
) + $fixLines | Set-Content -LiteralPath (Join-Path $runDir "final-summary.md")

$evidenceLines = foreach ($stepItem in $record.steps) {
    $evidenceItems = @($stepItem.evidence | Where-Object { $null -ne $_ -and $_ -ne "" })
    if (@($evidenceItems).Count -gt 0) {
        foreach ($item in $evidenceItems) {
            "- [$($stepItem.id)] $item"
        }
    }
}
if (@($evidenceLines).Count -eq 0) {
    $evidenceLines = @("- No evidence recorded yet.")
}

@(
    "# Evidence Log"
    ""
    "- Run ID: $($record.runId)"
    ""
    "## Evidence Items"
    ""
) + $evidenceLines | Set-Content -LiteralPath (Join-Path $runDir "evidence-log.md")

@(
    "# Issues Found"
    ""
    "- Run ID: $($record.runId)"
    ""
    "## Issues"
    ""
) + $issueLines | Set-Content -LiteralPath (Join-Path $runDir "issues-found.md")

[pscustomobject]@{
    RunId = $record.runId
    StepId = $StepId
    Status = $Status
    OverallResult = $record.overallResult
} | ConvertTo-Json -Depth 4
