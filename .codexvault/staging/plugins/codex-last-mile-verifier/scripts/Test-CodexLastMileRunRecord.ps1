[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$RunRecordPath
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

if (-not (Test-Path -LiteralPath $RunRecordPath)) {
    throw "Run record not found: $RunRecordPath"
}

$record = Get-Content -LiteralPath $RunRecordPath -Raw | ConvertFrom-Json

function Test-HasProperty {
    param(
        [object]$Object,
        [string]$Name
    )

    return $null -ne $Object.PSObject.Properties[$Name]
}

$requiredTopLevel = @(
    "schemaVersion",
    "runId",
    "pluginVersion",
    "createdAt",
    "updatedAt",
    "status",
    "overallResult",
    "target",
    "preflight",
    "stepOrder",
    "steps",
    "smokeTest",
    "issues",
    "recommendedFixes",
    "assumptions",
    "artifacts",
    "artifactPath"
)

foreach ($field in $requiredTopLevel) {
    if (-not (Test-HasProperty -Object $record -Name $field)) {
        throw "Missing required field '$field' in run record."
    }
}

if ($record.runId -notmatch '^clmv-[a-z0-9\-]+-\d{8}T\d{6}Z-[a-z0-9]{6}$') {
    throw "Run ID format is invalid: $($record.runId)"
}

$allowedOverallResults = @("pending", "in-progress", "pass", "fail", "blocked")
if ($allowedOverallResults -notcontains $record.overallResult) {
    throw "Overall result must be one of: $($allowedOverallResults -join ', ')"
}

$allowedStatuses = @("initialized", "running", "completed")
if ($allowedStatuses -notcontains $record.status) {
    throw "Status must be one of: $($allowedStatuses -join ', ')"
}

$allowedStepStatuses = @("pass", "fail", "blocked", "not-run")
foreach ($step in $record.steps) {
    if ($allowedStepStatuses -notcontains $step.status) {
        throw "Invalid step status '$($step.status)' for step '$($step.id)'."
    }
}

$requiredArtifactFields = @(
    "checklist",
    "finalSummary",
    "evidenceLog",
    "issuesLog",
    "runRecord",
    "attachments"
)

foreach ($field in $requiredArtifactFields) {
    if (-not (Test-HasProperty -Object $record.artifacts -Name $field)) {
        throw "Missing required artifact field '$field'."
    }
}

[pscustomobject]@{
    Valid = $true
    RunId = $record.runId
    OverallResult = $record.overallResult
} | ConvertTo-Json -Depth 4
