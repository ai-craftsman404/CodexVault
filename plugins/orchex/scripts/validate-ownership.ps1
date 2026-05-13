[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$RunPath
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$resolvedRunPath = (Resolve-Path -LiteralPath $RunPath).Path
$ledgerPath = Join-Path $resolvedRunPath "task-ledger.md"

if (-not (Test-Path -LiteralPath $ledgerPath)) {
    [pscustomobject]@{
        ok = $true
        overlaps = @()
        ownershipLines = 0
        reason = "No task-ledger.md present."
    } | ConvertTo-Json -Depth 5
    exit 0
}

$content = Get-Content -LiteralPath $ledgerPath -Raw
$ownershipMatches = [regex]::Matches($content, '(?im)^\s*Owner:\s*(?<owner>[^|]+?)\s*\|\s*Files:\s*(?<files>.+?)\s*$')

if ($ownershipMatches.Count -eq 0) {
    [pscustomobject]@{
        ok = $true
        overlaps = @()
        ownershipLines = 0
        reason = "No multi-agent ownership lines declared."
    } | ConvertTo-Json -Depth 5
    exit 0
}

$fileOwners = @{}
$overlaps = New-Object System.Collections.ArrayList

foreach ($ownershipMatch in $ownershipMatches) {
    $owner = $ownershipMatch.Groups["owner"].Value.Trim()
    $files = $ownershipMatch.Groups["files"].Value.Split(",") | ForEach-Object { $_.Trim() } | Where-Object { $_ }

    foreach ($file in $files) {
        $normalizedFile = $file.ToLowerInvariant()
        if ($fileOwners.ContainsKey($normalizedFile)) {
            $existingOwner = $fileOwners[$normalizedFile]
            if ($existingOwner -ne $owner) {
                [void]$overlaps.Add([pscustomobject]@{
                    file = $file
                    owners = @($existingOwner, $owner)
                })
            }
        }
        else {
            $fileOwners[$normalizedFile] = $owner
        }
    }
}

[pscustomobject]@{
    ok = ($overlaps.Count -eq 0)
    overlaps = @($overlaps)
    ownershipLines = $ownershipMatches.Count
    reason = $(if ($overlaps.Count -eq 0) { "Ownership validation passed." } else { "Overlapping ownership detected." })
} | ConvertTo-Json -Depth 5

if ($overlaps.Count -gt 0) {
    exit 1
}
