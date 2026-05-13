[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$TargetName,

    [Parameter(Mandatory = $true)]
    [ValidateSet("plugin", "skill")]
    [string]$TargetType,

    [Parameter(Mandatory = $true)]
    [string]$LocalPath,

    [Parameter(Mandatory = $true)]
    [string]$ExpectedEntrypoint,

    [Parameter(Mandatory = $true)]
    [string]$ExpectedInvocationMethod,

    [Parameter(Mandatory = $true)]
    [string]$ExpectedDisplayName,

    [Parameter(Mandatory = $true)]
    [string]$ExpectedShortDescription,

    [string]$PluginVersion = "0.1.0"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$pluginRoot = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
$runsRoot = Join-Path $pluginRoot "runs"
$registryRunsRoot = Join-Path $pluginRoot "registry\\runs"
$qualityLogPath = Join-Path $pluginRoot "registry\\quality-review-log.json"

$normalizedSlug = ($TargetName.ToLowerInvariant() -replace '[^a-z0-9\-]+', '-') -replace '(^-+|-+$)', ''
if ([string]::IsNullOrWhiteSpace($normalizedSlug)) {
    throw "TargetName must contain at least one alphanumeric character."
}

$timestamp = (Get-Date).ToUniversalTime()
$timestampCompact = $timestamp.ToString("yyyyMMddTHHmmssZ")
$year = $timestamp.ToString("yyyy")
$month = $timestamp.ToString("MM")
$shortId = [guid]::NewGuid().ToString("N").Substring(0, 6)
$runId = "clmv-$normalizedSlug-$timestampCompact-$shortId"
$runDir = Join-Path (Join-Path (Join-Path $runsRoot $year) $month) $runId

New-Item -ItemType Directory -Path $runDir -Force | Out-Null
New-Item -ItemType Directory -Path (Join-Path $runDir "attachments") -Force | Out-Null
New-Item -ItemType Directory -Path $registryRunsRoot -Force | Out-Null

$resolvedLocalPath = if ([System.IO.Path]::IsPathRooted($LocalPath)) {
    [System.IO.Path]::GetFullPath($LocalPath)
} else {
    [System.IO.Path]::GetFullPath((Join-Path (Get-Location) $LocalPath))
}
$entrypointPath = if ([System.IO.Path]::IsPathRooted($ExpectedEntrypoint)) {
    $ExpectedEntrypoint
} else {
    Join-Path $resolvedLocalPath $ExpectedEntrypoint
}

$steps = @(
    [ordered]@{ id = "discovery-surface"; label = "Appears in Codex discovery surface"; status = "not-run"; notes = @(); evidence = @() }
    [ordered]@{ id = "display-name"; label = "Display name matches expectation"; status = "not-run"; notes = @(); evidence = @() }
    [ordered]@{ id = "description"; label = "Short description matches expectation"; status = "not-run"; notes = @(); evidence = @() }
    [ordered]@{ id = "install-action"; label = "Install action is available"; status = "not-run"; notes = @(); evidence = @() }
    [ordered]@{ id = "install-complete"; label = "Installation completes"; status = "not-run"; notes = @(); evidence = @() }
    [ordered]@{ id = "invocation-available"; label = "Post-install invocation is available"; status = "not-run"; notes = @(); evidence = @() }
    [ordered]@{ id = "smoke-test"; label = "Smoke-test invocation behaves as expected"; status = "not-run"; notes = @(); evidence = @() }
)

$record = [ordered]@{
    schemaVersion = "1.0"
    runId = $runId
    pluginVersion = $PluginVersion
    createdAt = $timestamp.ToString("o")
    updatedAt = $timestamp.ToString("o")
    status = "initialized"
    overallResult = "pending"
    target = [ordered]@{
        name = $TargetName
        type = $TargetType
        localPath = $resolvedLocalPath
        expectedEntrypoint = $entrypointPath
        expectedInvocationMethod = $ExpectedInvocationMethod
        expectedDisplayName = $ExpectedDisplayName
        expectedShortDescription = $ExpectedShortDescription
    }
    preflight = [ordered]@{
        localPathExists = (Test-Path -LiteralPath $resolvedLocalPath)
        entrypointExists = (Test-Path -LiteralPath $entrypointPath)
        notes = @()
    }
    stepOrder = @(
        "discovery-surface",
        "display-name",
        "description",
        "install-action",
        "install-complete",
        "invocation-available",
        "smoke-test"
    )
    steps = $steps
    smokeTest = [ordered]@{
        prompt = $null
        expectedBehavior = $null
        observedBehavior = $null
    }
    issues = @()
    recommendedFixes = @()
    assumptions = @()
    artifacts = [ordered]@{
        checklist = "checklist.md"
        finalSummary = "final-summary.md"
        evidenceLog = "evidence-log.md"
        issuesLog = "issues-found.md"
        runRecord = "run-record.json"
        attachments = "attachments/"
    }
    artifactPath = ("runs/{0}/{1}/{2}" -f $year, $month, $runId)
}

$recordPath = Join-Path $runDir "run-record.json"
$record | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $recordPath

$nowText = $timestamp.ToString("yyyy-MM-dd HH:mm:ss 'UTC'")

@(
    "# Codex Last-Mile Verification Checklist"
    ""
    "- Run ID: $runId"
    "- Created: $nowText"
    "- Target: $TargetName ($TargetType)"
    "- Local path: $resolvedLocalPath"
    "- Expected entrypoint: $entrypointPath"
    "- Expected invocation: $ExpectedInvocationMethod"
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
    "| Appears in Codex discovery surface | not-run |  |"
    "| Display name matches expectation | not-run |  |"
    "| Short description matches expectation | not-run |  |"
    "| Install action is available | not-run |  |"
    "| Installation completes | not-run |  |"
    "| Post-install invocation is available | not-run |  |"
    "| Smoke-test invocation behaves as expected | not-run |  |"
) | Set-Content -LiteralPath (Join-Path $runDir "checklist.md")

@(
    "# Final Verification Summary"
    ""
    "- Run ID: $runId"
    "- Created: $nowText"
    "- Overall result: pending"
    ""
    "## Outcome"
    ""
    "- Replace this section with the final pass, fail, or blocked summary."
    ""
    "## Step Results"
    ""
    "- Record pass/fail/blocked notes for each live step."
    ""
    "## Issues Found"
    ""
    "- Add issues here."
    ""
    "## Recommended Fixes"
    ""
    "- Add concrete fixes here."
) | Set-Content -LiteralPath (Join-Path $runDir "final-summary.md")

@(
    "# Evidence Log"
    ""
    "- Run ID: $runId"
    ""
    "## Evidence Items"
    ""
    "- Add screenshots, observed runtime text, and smoke-test prompts/results here."
) | Set-Content -LiteralPath (Join-Path $runDir "evidence-log.md")

@(
    "# Issues Found"
    ""
    "- Run ID: $runId"
    ""
    "## Issues"
    ""
    "- Add one issue per bullet, with the affected step and recommended fix."
) | Set-Content -LiteralPath (Join-Path $runDir "issues-found.md")

if (-not (Test-Path -LiteralPath $qualityLogPath)) {
    (@{
        items = @()
    } | ConvertTo-Json -Depth 4) | Set-Content -LiteralPath $qualityLogPath
}

[pscustomobject]@{
    RunId = $runId
    RunPath = $runDir
    RecordPath = $recordPath
} | ConvertTo-Json -Depth 4
