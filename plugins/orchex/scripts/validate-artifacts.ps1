[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$RunPath,

    [Parameter(Mandatory = $true)]
    [ValidateSet("plan", "build", "test", "review", "done")]
    [string]$Stage
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Get-RunMetadata {
    param([string]$ResolvedRunPath)

    $metadataPath = Join-Path $ResolvedRunPath "run-metadata.json"
    if (-not (Test-Path -LiteralPath $metadataPath)) {
        throw "run-metadata.json is missing."
    }

    $metadata = Get-Content -LiteralPath $metadataPath -Raw | ConvertFrom-Json
    if (-not $metadata.runId -or -not $metadata.createdAt -or -not $metadata.orchestrator) {
        throw "run-metadata.json is missing required fields."
    }

    return $metadata
}

function Test-MeaningfulContent {
    param([string]$Content)

    if ([string]::IsNullOrWhiteSpace($Content)) {
        return $false
    }

    $trimmed = $Content.Trim()
    if ($trimmed.Length -lt 4) {
        return $false
    }

    if ($trimmed -match "(?im)^\s*\[TODO:.*\]\s*$") {
        return $false
    }

    if ($trimmed -match "(?im)^\s*TODO[:\s]") {
        return $false
    }

    $meaningfulLines = @(
        $trimmed -split "`r?`n" |
        Where-Object {
            $line = $_.Trim()
            $line -and
            $line -notmatch '^#+\s*$' -and
            $line -notmatch '^\[TODO:.*\]$'
        }
    )

    return ($meaningfulLines.Count -gt 0)
}

$requiredByStage = @{
    plan   = @("run-metadata.json", "plan.md", "task-ledger.md")
    build  = @("run-metadata.json", "plan.md", "task-ledger.md", "build-log.md")
    test   = @("run-metadata.json", "plan.md", "task-ledger.md", "build-log.md", "test-report.md")
    review = @("run-metadata.json", "plan.md", "task-ledger.md", "build-log.md", "test-report.md", "review.md")
    done   = @("run-metadata.json", "plan.md", "task-ledger.md", "build-log.md", "test-report.md", "review.md", "run-summary.md")
}

$resolvedRunPath = (Resolve-Path -LiteralPath $RunPath).Path
$metadataErrors = New-Object System.Collections.Generic.List[string]
$runId = $null

try {
    $metadata = Get-RunMetadata -ResolvedRunPath $resolvedRunPath
    $runId = [string]$metadata.runId
}
catch {
    $metadataErrors.Add($_.Exception.Message)
}

$missing = New-Object System.Collections.Generic.List[string]

foreach ($fileName in $requiredByStage[$Stage]) {
    $filePath = Join-Path $resolvedRunPath $fileName
    if (-not (Test-Path -LiteralPath $filePath)) {
        $missing.Add($fileName)
        continue
    }

    if ($fileName -eq "run-metadata.json") {
        continue
    }

    $content = Get-Content -LiteralPath $filePath -Raw
    if (-not (Test-MeaningfulContent -Content $content)) {
        $missing.Add($fileName)
        continue
    }

    if ($runId -and $content -notmatch ("(?im)^\s*Run ID:\s*" + [regex]::Escape($runId) + "\s*$")) {
        $missing.Add($fileName)
        continue
    }

    if ($fileName -eq "task-ledger.md" -and $content -notmatch "(?im)^\s*Current Stage:\s*\S+") {
        $missing.Add($fileName)
    }
}

$result = [pscustomobject]@{
    ok             = ($missing.Count -eq 0 -and $metadataErrors.Count -eq 0)
    stage          = $Stage
    missing        = @($missing)
    metadataErrors = @($metadataErrors)
}

$result | ConvertTo-Json -Depth 4

if ($missing.Count -gt 0 -or $metadataErrors.Count -gt 0) {
    exit 1
}
