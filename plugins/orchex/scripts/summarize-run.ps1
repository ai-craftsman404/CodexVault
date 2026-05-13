[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$RunPath,

    [string]$OutputFile = "run-summary.md"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$resolvedRunPath = (Resolve-Path -LiteralPath $RunPath).Path
$summaryPath = Join-Path $resolvedRunPath $OutputFile
$metadataPath = Join-Path $resolvedRunPath "run-metadata.json"
$metadata = Get-Content -LiteralPath $metadataPath -Raw | ConvertFrom-Json

function Read-Artifact {
    param([string]$Name)
    $path = Join-Path $resolvedRunPath $Name
    if (Test-Path -LiteralPath $path) {
        return Get-Content -LiteralPath $path -Raw
    }
    return ""
}

$plan = Read-Artifact "plan.md"
$ledger = Read-Artifact "task-ledger.md"
$buildLog = Read-Artifact "build-log.md"
$testReport = Read-Artifact "test-report.md"
$review = Read-Artifact "review.md"

$testResult = if ($testReport -match "RESULT:\s*(PASS|FAIL)") { $matches[1] } else { "UNKNOWN" }
$reviewVerdict = if ($review -match "Verdict:\s*(.+)") { $matches[1].Trim() } else { "Not recorded" }

$summary = @"
# Run Summary

- Run ID: $($metadata.runId)
- Run path: `$resolvedRunPath`
- Test result: $testResult
- Review verdict: $reviewVerdict

## Artifact Status

- plan.md: $(if ($plan) { "present" } else { "missing" })
- task-ledger.md: $(if ($ledger) { "present" } else { "missing" })
- build-log.md: $(if ($buildLog) { "present" } else { "missing" })
- test-report.md: $(if ($testReport) { "present" } else { "missing" })
- review.md: $(if ($review) { "present" } else { "missing" })

## Notes

$(if ($ledger) { $ledger.Trim() } else { "No task ledger recorded." })
"@

Set-Content -LiteralPath $summaryPath -Value $summary
$summaryPath
