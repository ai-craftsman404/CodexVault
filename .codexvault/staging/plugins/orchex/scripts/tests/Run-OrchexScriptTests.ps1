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
    $output = & powershell -NoProfile -ExecutionPolicy Bypass -File $scriptPath @Arguments 2>&1
    [pscustomobject]@{
        ExitCode = $LASTEXITCODE
        Output   = ($output | Out-String).Trim()
    }
}

function New-RunDirectory {
    $path = Join-Path ([System.IO.Path]::GetTempPath()) ("orchex-test-" + [guid]::NewGuid().ToString("N"))
    New-Item -ItemType Directory -Path $path | Out-Null
    return $path
}

function Write-Artifact {
    param(
        [string]$RunPath,
        [string]$Name,
        [string]$Content
    )

    Set-Content -LiteralPath (Join-Path $RunPath $Name) -Value $Content
}

function Write-RunMetadata {
    param(
        [string]$RunPath,
        [string]$RunId = "run-123"
    )

    Set-Content -LiteralPath (Join-Path $RunPath "run-metadata.json") -Value (@{
        runId        = $RunId
        createdAt    = "2026-04-30T10:00:00Z"
        orchestrator = "orchex"
    } | ConvertTo-Json)
}

function Test-NodeProfileDetection {
    $repoPath = New-RunDirectory
    try {
        Set-Content -LiteralPath (Join-Path $repoPath "package.json") -Value '{ "scripts": { "test": "vitest", "build": "vite build", "lint": "eslint ." } }'
        $result = Invoke-Script -ScriptName "resolve-stack-profile.ps1" -Arguments @("-RepoPath", $repoPath)
        Assert-True ($result.ExitCode -eq 0) "Stack profile detection should succeed."
        $profile = $result.Output | ConvertFrom-Json
        Assert-True ($profile.name -eq "node") "Expected node profile."
        Assert-True ($profile.testCommand -eq "npm test") "Expected npm test command."
        $script:testsRun++
    }
    finally {
        Remove-Item -LiteralPath $repoPath -Recurse -Force
    }
}

function Test-ArtifactValidationFailure {
    $runPath = New-RunDirectory
    try {
        Write-RunMetadata -RunPath $runPath
        Write-Artifact -RunPath $runPath -Name "plan.md" -Content "Run ID: run-123`nPlan"
        $result = Invoke-Script -ScriptName "validate-artifacts.ps1" -Arguments @("-RunPath", $runPath, "-Stage", "plan")
        Assert-True ($result.ExitCode -ne 0) "Artifact validation should fail when task-ledger.md is missing."
        Assert-True ($result.Output -match "task-ledger.md") "Expected missing task-ledger.md in output."
        $script:testsRun++
    }
    finally {
        Remove-Item -LiteralPath $runPath -Recurse -Force
    }
}

function Test-PlaceholderArtifactFails {
    $runPath = New-RunDirectory
    try {
        Write-RunMetadata -RunPath $runPath
        Write-Artifact -RunPath $runPath -Name "plan.md" -Content "#`n"
        Write-Artifact -RunPath $runPath -Name "task-ledger.md" -Content "Run ID: run-123`nTODO: fill later"
        $result = Invoke-Script -ScriptName "validate-artifacts.ps1" -Arguments @("-RunPath", $runPath, "-Stage", "plan")
        Assert-True ($result.ExitCode -ne 0) "Placeholder artifacts should fail validation."
        $script:testsRun++
    }
    finally {
        Remove-Item -LiteralPath $runPath -Recurse -Force
    }
}

function Test-InvalidTransitionFails {
    $runPath = New-RunDirectory
    try {
        $result = Invoke-Script -ScriptName "validate-stage.ps1" -Arguments @("-RunPath", $runPath, "-CurrentStage", "plan", "-TargetStage", "review")
        Assert-True ($result.ExitCode -ne 0) "Invalid transition should fail."
        Assert-True ($result.Output -match "Unsupported stage transition") "Expected invalid transition message."
        $script:testsRun++
    }
    finally {
        Remove-Item -LiteralPath $runPath -Recurse -Force
    }
}

function Test-ReviewRequiresPassingEvidence {
    $runPath = New-RunDirectory
    try {
        Write-RunMetadata -RunPath $runPath
        Write-Artifact -RunPath $runPath -Name "plan.md" -Content "Run ID: run-123`nPlan"
        Write-Artifact -RunPath $runPath -Name "task-ledger.md" -Content "Run ID: run-123`nCurrent Stage: test`nLedger"
        Write-Artifact -RunPath $runPath -Name "build-log.md" -Content "Run ID: run-123`nBuild"
        Write-Artifact -RunPath $runPath -Name "test-report.md" -Content "Run ID: run-123`nRESULT: PASS"
        $result = Invoke-Script -ScriptName "validate-stage.ps1" -Arguments @("-RunPath", $runPath, "-CurrentStage", "test", "-TargetStage", "review")
        Assert-True ($result.ExitCode -ne 0) "Review transition should fail without evidence."
        Assert-True ($result.Output -match "missing execution evidence") "Expected evidence failure."
        $script:testsRun++
    }
    finally {
        Remove-Item -LiteralPath $runPath -Recurse -Force
    }
}

function Test-ReviewTransitionPasses {
    $runPath = New-RunDirectory
    try {
        Write-RunMetadata -RunPath $runPath
        Write-Artifact -RunPath $runPath -Name "plan.md" -Content "Run ID: run-123`nPlan"
        Write-Artifact -RunPath $runPath -Name "task-ledger.md" -Content "Run ID: run-123`nCurrent Stage: test`nLedger"
        Write-Artifact -RunPath $runPath -Name "build-log.md" -Content "Run ID: run-123`nBuild"
        Write-Artifact -RunPath $runPath -Name "test-report.md" -Content "Run ID: run-123`nRESULT: PASS`nEVIDENCE: npm test"
        $result = Invoke-Script -ScriptName "validate-stage.ps1" -Arguments @("-RunPath", $runPath, "-CurrentStage", "test", "-TargetStage", "review")
        Assert-True ($result.ExitCode -eq 0) "Review transition should pass with evidence."
        $script:testsRun++
    }
    finally {
        Remove-Item -LiteralPath $runPath -Recurse -Force
    }
}

function Test-LedgerStageMismatchFails {
    $runPath = New-RunDirectory
    try {
        Write-RunMetadata -RunPath $runPath
        Write-Artifact -RunPath $runPath -Name "plan.md" -Content "Run ID: run-123`nPlan"
        Write-Artifact -RunPath $runPath -Name "task-ledger.md" -Content "Run ID: run-123`nCurrent Stage: review`nLedger"
        $result = Invoke-Script -ScriptName "validate-stage.ps1" -Arguments @("-RunPath", $runPath, "-CurrentStage", "plan", "-TargetStage", "build")
        Assert-True ($result.ExitCode -ne 0) "Ledger stage mismatch should fail validation."
        Assert-True ($result.Output -match "does not match requested current stage") "Expected ledger mismatch failure."
        $script:testsRun++
    }
    finally {
        Remove-Item -LiteralPath $runPath -Recurse -Force
    }
}

function Test-OwnershipConflictFails {
    $runPath = New-RunDirectory
    try {
        Write-RunMetadata -RunPath $runPath
        Write-Artifact -RunPath $runPath -Name "plan.md" -Content "Run ID: run-123`nPlan"
        Write-Artifact -RunPath $runPath -Name "task-ledger.md" -Content "Run ID: run-123`nCurrent Stage: plan`nOwner: planner | Files: docs/plan.md, src/app.ts`nOwner: coder | Files: src/app.ts"
        $result = Invoke-Script -ScriptName "validate-ownership.ps1" -Arguments @("-RunPath", $runPath)
        Assert-True ($result.ExitCode -ne 0) "Ownership conflict should fail validation."
        Assert-True ($result.Output -match "Overlapping ownership detected") "Expected overlap failure."
        $script:testsRun++
    }
    finally {
        Remove-Item -LiteralPath $runPath -Recurse -Force
    }
}

function Test-OwnershipValidationPasses {
    $runPath = New-RunDirectory
    try {
        Write-RunMetadata -RunPath $runPath
        Write-Artifact -RunPath $runPath -Name "plan.md" -Content "Run ID: run-123`nPlan"
        Write-Artifact -RunPath $runPath -Name "task-ledger.md" -Content "Run ID: run-123`nCurrent Stage: plan`nOwner: planner | Files: docs/plan.md`nOwner: coder | Files: src/app.ts, tests/app.test.ts"
        $result = Invoke-Script -ScriptName "validate-ownership.ps1" -Arguments @("-RunPath", $runPath)
        Assert-True ($result.ExitCode -eq 0) "Non-overlapping ownership should pass validation."
        $script:testsRun++
    }
    finally {
        Remove-Item -LiteralPath $runPath -Recurse -Force
    }
}

function Test-CompletionRequiresApprovalWhenConfigured {
    $runPath = New-RunDirectory
    try {
        Write-RunMetadata -RunPath $runPath
        Write-Artifact -RunPath $runPath -Name "plan.md" -Content "Run ID: run-123`nPlan"
        Write-Artifact -RunPath $runPath -Name "task-ledger.md" -Content "Run ID: run-123`nCurrent Stage: review`nLedger"
        Write-Artifact -RunPath $runPath -Name "build-log.md" -Content "Run ID: run-123`nBuild"
        Write-Artifact -RunPath $runPath -Name "test-report.md" -Content "Run ID: run-123`nRESULT: PASS`nEVIDENCE: npm test"
        Write-Artifact -RunPath $runPath -Name "review.md" -Content "Run ID: run-123`nVerdict: Approved"
        $result = Invoke-Script -ScriptName "validate-stage.ps1" -Arguments @("-RunPath", $runPath, "-CurrentStage", "review", "-TargetStage", "done", "-RequireApproval")
        Assert-True ($result.ExitCode -ne 0) "Completion should fail without approval when approval is required."
        Assert-True ($result.Output -match "approval-note.md") "Expected approval-note.md failure."
        $script:testsRun++
    }
    finally {
        Remove-Item -LiteralPath $runPath -Recurse -Force
    }
}

function Test-SummaryGeneration {
    $runPath = New-RunDirectory
    try {
        Write-RunMetadata -RunPath $runPath
        Write-Artifact -RunPath $runPath -Name "plan.md" -Content "Run ID: run-123`nPlan"
        Write-Artifact -RunPath $runPath -Name "task-ledger.md" -Content "Run ID: run-123`nCurrent Stage: review"
        Write-Artifact -RunPath $runPath -Name "build-log.md" -Content "Run ID: run-123`nBuild"
        Write-Artifact -RunPath $runPath -Name "test-report.md" -Content "Run ID: run-123`nRESULT: PASS`nEVIDENCE: npm test"
        Write-Artifact -RunPath $runPath -Name "review.md" -Content "Run ID: run-123`nVerdict: Approved"
        $result = Invoke-Script -ScriptName "summarize-run.ps1" -Arguments @("-RunPath", $runPath)
        Assert-True ($result.ExitCode -eq 0) "Summary generation should succeed."
        $summaryPath = Join-Path $runPath "run-summary.md"
        Assert-True (Test-Path -LiteralPath $summaryPath) "Summary file should exist."
        $summaryContent = Get-Content -LiteralPath $summaryPath -Raw
        Assert-True ($summaryContent -match "Run ID: run-123") "Summary should include the run ID."
        Assert-True ($summaryContent -match "Test result: PASS") "Summary should include the passing test result."
        $script:testsRun++
    }
    finally {
        Remove-Item -LiteralPath $runPath -Recurse -Force
    }
}

function Test-UnsupportedStackFailsClosed {
    $repoPath = New-RunDirectory
    try {
        Set-Content -LiteralPath (Join-Path $repoPath "README.md") -Value "Unknown repo"
        $result = Invoke-Script -ScriptName "resolve-stack-profile.ps1" -Arguments @("-RepoPath", $repoPath)
        Assert-True ($result.ExitCode -eq 0) "Profile detection should still return a result object."
        $profile = $result.Output | ConvertFrom-Json
        Assert-True (-not $profile.supported) "Unsupported repo should fail closed."
        Assert-True ($profile.name -eq "unknown") "Expected unknown profile."
        $script:testsRun++
    }
    finally {
        Remove-Item -LiteralPath $repoPath -Recurse -Force
    }
}

function Test-StaleArtifactRunIdMismatchFails {
    $runPath = New-RunDirectory
    try {
        Write-RunMetadata -RunPath $runPath -RunId "run-999"
        Write-Artifact -RunPath $runPath -Name "plan.md" -Content "Run ID: run-123`nPlan"
        Write-Artifact -RunPath $runPath -Name "task-ledger.md" -Content "Run ID: run-123`nCurrent Stage: plan`nLedger"
        $result = Invoke-Script -ScriptName "validate-artifacts.ps1" -Arguments @("-RunPath", $runPath, "-Stage", "plan")
        Assert-True ($result.ExitCode -ne 0) "Run ID mismatch should fail validation."
        $script:testsRun++
    }
    finally {
        Remove-Item -LiteralPath $runPath -Recurse -Force
    }
}

function Test-MissingRunMetadataFails {
    $runPath = New-RunDirectory
    try {
        Write-Artifact -RunPath $runPath -Name "plan.md" -Content "Run ID: run-123`nPlan"
        Write-Artifact -RunPath $runPath -Name "task-ledger.md" -Content "Run ID: run-123`nCurrent Stage: plan`nLedger"
        $result = Invoke-Script -ScriptName "validate-artifacts.ps1" -Arguments @("-RunPath", $runPath, "-Stage", "plan")
        Assert-True ($result.ExitCode -ne 0) "Missing run metadata should fail validation."
        Assert-True ($result.Output -match "run-metadata.json") "Expected run metadata failure."
        $script:testsRun++
    }
    finally {
        Remove-Item -LiteralPath $runPath -Recurse -Force
    }
}

Test-NodeProfileDetection
Test-ArtifactValidationFailure
Test-PlaceholderArtifactFails
Test-InvalidTransitionFails
Test-ReviewRequiresPassingEvidence
Test-ReviewTransitionPasses
Test-LedgerStageMismatchFails
Test-OwnershipConflictFails
Test-OwnershipValidationPasses
Test-CompletionRequiresApprovalWhenConfigured
Test-SummaryGeneration
Test-UnsupportedStackFailsClosed
Test-StaleArtifactRunIdMismatchFails
Test-MissingRunMetadataFails

Write-Host "Orchex script tests passed: $testsRun"
