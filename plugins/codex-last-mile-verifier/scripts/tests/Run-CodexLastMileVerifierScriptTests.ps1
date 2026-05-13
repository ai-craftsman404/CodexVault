[CmdletBinding()]
param()

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$scriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$pluginRoot = Split-Path -Parent (Split-Path -Parent $scriptRoot)
$scriptsRoot = Join-Path $pluginRoot "scripts"

$testsRun = 0

function Assert-True {
    param(
        [bool]$Condition,
        [string]$Message
    )

    if (-not $Condition) {
        throw $Message
    }
}

function Invoke-Script {
    param(
        [string]$ScriptName,
        [string[]]$Arguments
    )

    $scriptPath = Join-Path $scriptsRoot $ScriptName
    $previousErrorActionPreference = $ErrorActionPreference
    $ErrorActionPreference = "Continue"
    try {
        $output = & powershell -NoProfile -ExecutionPolicy Bypass -File $scriptPath @Arguments 2>&1 | Out-String
    }
    finally {
        $ErrorActionPreference = $previousErrorActionPreference
    }

    [pscustomobject]@{
        ExitCode = $LASTEXITCODE
        Output = $output.Trim()
    }
}

function Test-RunInitialization {
    $localPath = Join-Path $pluginRoot "skills"
    $result = Invoke-Script -ScriptName "New-CodexLastMileRun.ps1" -Arguments @(
        "-TargetName", "Sample Skill",
        "-TargetType", "skill",
        "-LocalPath", $localPath,
        "-ExpectedEntrypoint", "codex-last-mile-verifier\\SKILL.md",
        "-ExpectedInvocationMethod", '$codex-last-mile-verifier',
        "-ExpectedDisplayName", "Codex Last-Mile Verifier",
        "-ExpectedShortDescription", "Standardize real Codex discovery, install, and smoke-test verification for plugins and skills."
    )
    Assert-True ($result.ExitCode -eq 0) "Run initialization should succeed."

    $created = $result.Output | ConvertFrom-Json
    Assert-True ([string]::IsNullOrWhiteSpace($created.RunId) -eq $false) "RunId should be returned."
    Assert-True (Test-Path -LiteralPath $created.RunPath) "Run directory should exist."
    Assert-True (Test-Path -LiteralPath $created.RecordPath) "Run record should exist."
    Assert-True (Test-Path -LiteralPath (Join-Path $created.RunPath "checklist.md")) "Checklist should exist."
    $script:testsRun++

    return $created
}

function Test-StepUpdate {
    param([pscustomobject]$CreatedRun)

    $result = Invoke-Script -ScriptName "Set-CodexLastMileStepStatus.ps1" -Arguments @(
        "-RunRecordPath", $CreatedRun.RecordPath,
        "-StepId", "discovery-surface",
        "-Status", "pass",
        "-Note", "Target appeared in the skills library.",
        "-EvidenceItem", "Manual observation recorded."
    )
    Assert-True ($result.ExitCode -eq 0) "Step update should succeed."
    $updated = Get-Content -LiteralPath $CreatedRun.RecordPath -Raw | ConvertFrom-Json
    $step = $updated.steps | Where-Object { $_.id -eq "discovery-surface" } | Select-Object -First 1
    Assert-True ($step.status -eq "pass") "Step status should be updated."
    $script:testsRun++
}

function Test-RunRecordValidation {
    param([pscustomobject]$CreatedRun)

    $result = Invoke-Script -ScriptName "Test-CodexLastMileRunRecord.ps1" -Arguments @("-RunRecordPath", $CreatedRun.RecordPath)
    Assert-True ($result.ExitCode -eq 0) "Run record validation should succeed."
    $script:testsRun++
}

function Test-RegistryUpdate {
    param([pscustomobject]$CreatedRun)

    $result = Invoke-Script -ScriptName "Update-CodexLastMileRegistry.ps1" -Arguments @("-RunRecordPath", $CreatedRun.RecordPath)
    Assert-True ($result.ExitCode -eq 0) "Registry update should succeed."

    $indexPath = Join-Path $pluginRoot "registry\\runs\\index.jsonl"
    Assert-True (Test-Path -LiteralPath $indexPath) "Registry index should exist."
    $content = Get-Content -LiteralPath $indexPath -Raw
    Assert-True ($content -match $CreatedRun.RunId) "Registry should contain the run ID."
    $script:testsRun++
}

function Test-InvalidStatusFailsValidation {
    param([pscustomobject]$CreatedRun)

    $record = Get-Content -LiteralPath $CreatedRun.RecordPath -Raw | ConvertFrom-Json
    $record.steps[0].status = "maybe"
    $record | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $CreatedRun.RecordPath

    $result = Invoke-Script -ScriptName "Test-CodexLastMileRunRecord.ps1" -Arguments @("-RunRecordPath", $CreatedRun.RecordPath)
    Assert-True ($result.ExitCode -ne 0) "Invalid step status should fail validation."
    $script:testsRun++
}

$indexPath = Join-Path $pluginRoot "registry\\runs\\index.jsonl"
$indexBackup = if (Test-Path -LiteralPath $indexPath) { Get-Content -LiteralPath $indexPath -Raw } else { $null }

$createdRun = Test-RunInitialization
try {
    Test-StepUpdate -CreatedRun $createdRun
    Test-RunRecordValidation -CreatedRun $createdRun
    Test-RegistryUpdate -CreatedRun $createdRun
    Test-InvalidStatusFailsValidation -CreatedRun $createdRun
}
finally {
    if ($null -eq $indexBackup) {
        if (Test-Path -LiteralPath $indexPath) {
            Remove-Item -LiteralPath $indexPath -Force
        }
    }
    else {
        Set-Content -LiteralPath $indexPath -Value $indexBackup
    }

    if ($createdRun -and (Test-Path -LiteralPath $createdRun.RunPath)) {
        Remove-Item -LiteralPath $createdRun.RunPath -Recurse -Force
    }
}

Write-Host "Codex Last-Mile Verifier script tests passed: $testsRun"
