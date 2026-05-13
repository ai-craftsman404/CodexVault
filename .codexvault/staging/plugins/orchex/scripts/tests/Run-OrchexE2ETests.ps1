[CmdletBinding()]
param()

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$scriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$pluginRoot = Split-Path -Parent (Split-Path -Parent $scriptRoot)
$scriptsRoot = Join-Path $pluginRoot "scripts"
$fixturesRoot = Join-Path $scriptRoot "fixtures"
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
    $path = Join-Path ([System.IO.Path]::GetTempPath()) ("orchex-e2e-" + [guid]::NewGuid().ToString("N"))
    New-Item -ItemType Directory -Path $path | Out-Null
    return $path
}

function Write-RunMetadata {
    param(
        [string]$RunPath,
        [string]$RunId = "e2e-run-001"
    )

    Set-Content -LiteralPath (Join-Path $RunPath "run-metadata.json") -Value (@{
        runId        = $RunId
        createdAt    = "2026-04-30T11:00:00Z"
        orchestrator = "orchex"
    } | ConvertTo-Json)
}

function Write-Artifact {
    param(
        [string]$RunPath,
        [string]$Name,
        [string]$Content
    )

    Set-Content -LiteralPath (Join-Path $RunPath $Name) -Value $Content
}

function Initialize-RunArtifacts {
    param(
        [string]$RunPath,
        [string]$RunId,
        [string]$CurrentStage,
        [string]$TestEvidence = "npm test",
        [string]$ReviewVerdict = "Approved"
    )

    Write-RunMetadata -RunPath $RunPath -RunId $RunId
    Write-Artifact -RunPath $RunPath -Name "plan.md" -Content "Run ID: $RunId`nGoal: E2E flow"
    Write-Artifact -RunPath $RunPath -Name "task-ledger.md" -Content "Run ID: $RunId`nCurrent Stage: $CurrentStage`nOwner: e2e"
    Write-Artifact -RunPath $RunPath -Name "build-log.md" -Content "Run ID: $RunId`nBuilt fixture flow"
    Write-Artifact -RunPath $RunPath -Name "test-report.md" -Content "Run ID: $RunId`nRESULT: PASS`nEVIDENCE: $TestEvidence"
    Write-Artifact -RunPath $RunPath -Name "review.md" -Content "Run ID: $RunId`nVerdict: $ReviewVerdict"
}

function Test-NodeFixtureEndToEnd {
    $repoPath = Join-Path $fixturesRoot "node-app"
    $runPath = New-RunDirectory
    try {
        $profileResult = Invoke-Script -ScriptName "resolve-stack-profile.ps1" -Arguments @("-RepoPath", $repoPath)
        Assert-True ($profileResult.ExitCode -eq 0) "Node fixture detection should succeed."
        $profile = $profileResult.Output | ConvertFrom-Json
        Assert-True ($profile.name -eq "node") "Expected node profile."

        Initialize-RunArtifacts -RunPath $runPath -RunId "node-e2e-001" -CurrentStage "test" -TestEvidence $profile.testCommand
        $transitionResult = Invoke-Script -ScriptName "validate-stage.ps1" -Arguments @("-RunPath", $runPath, "-CurrentStage", "test", "-TargetStage", "review")
        Assert-True ($transitionResult.ExitCode -eq 0) "Node fixture review transition should pass."

        $summaryResult = Invoke-Script -ScriptName "summarize-run.ps1" -Arguments @("-RunPath", $runPath)
        Assert-True ($summaryResult.ExitCode -eq 0) "Node fixture summary should succeed."
        $script:testsRun++
    }
    finally {
        Remove-Item -LiteralPath $runPath -Recurse -Force
    }
}

function Test-PythonFixtureEndToEnd {
    $repoPath = Join-Path $fixturesRoot "python-app"
    $runPath = New-RunDirectory
    try {
        $profileResult = Invoke-Script -ScriptName "resolve-stack-profile.ps1" -Arguments @("-RepoPath", $repoPath)
        Assert-True ($profileResult.ExitCode -eq 0) "Python fixture detection should succeed."
        $profile = $profileResult.Output | ConvertFrom-Json
        Assert-True ($profile.name -eq "python") "Expected python profile."

        Initialize-RunArtifacts -RunPath $runPath -RunId "python-e2e-001" -CurrentStage "review" -TestEvidence $profile.testCommand
        Write-Artifact -RunPath $runPath -Name "approval-note.md" -Content "Run ID: python-e2e-001`nApproved by: e2e"
        $transitionResult = Invoke-Script -ScriptName "validate-stage.ps1" -Arguments @("-RunPath", $runPath, "-CurrentStage", "review", "-TargetStage", "done", "-RequireApproval")
        Assert-True ($transitionResult.ExitCode -eq 0) "Python fixture completion should pass."

        $summaryResult = Invoke-Script -ScriptName "summarize-run.ps1" -Arguments @("-RunPath", $runPath)
        Assert-True ($summaryResult.ExitCode -eq 0) "Python fixture summary should succeed."
        $script:testsRun++
    }
    finally {
        Remove-Item -LiteralPath $runPath -Recurse -Force
    }
}

function Test-UnsupportedFixtureFailsClosed {
    $repoPath = Join-Path $fixturesRoot "unsupported-app"
    $profileResult = Invoke-Script -ScriptName "resolve-stack-profile.ps1" -Arguments @("-RepoPath", $repoPath)
    Assert-True ($profileResult.ExitCode -eq 0) "Unsupported fixture should still return a profile object."
    $profile = $profileResult.Output | ConvertFrom-Json
    Assert-True (-not $profile.supported) "Unsupported fixture should fail closed."
    Assert-True ($profile.name -eq "unknown") "Expected unknown profile."
    $script:testsRun++
}

function Test-EndToEndRejectsRunIdTamper {
    $repoPath = Join-Path $fixturesRoot "node-app"
    $runPath = New-RunDirectory
    try {
        $profileResult = Invoke-Script -ScriptName "resolve-stack-profile.ps1" -Arguments @("-RepoPath", $repoPath)
        Assert-True ($profileResult.ExitCode -eq 0) "Node fixture detection should succeed."
        $profile = $profileResult.Output | ConvertFrom-Json

        Initialize-RunArtifacts -RunPath $runPath -RunId "tamper-e2e-001" -CurrentStage "test" -TestEvidence $profile.testCommand
        Write-Artifact -RunPath $runPath -Name "test-report.md" -Content "Run ID: forged-run`nRESULT: PASS`nEVIDENCE: $($profile.testCommand)"
        $transitionResult = Invoke-Script -ScriptName "validate-stage.ps1" -Arguments @("-RunPath", $runPath, "-CurrentStage", "test", "-TargetStage", "review")
        Assert-True ($transitionResult.ExitCode -ne 0) "Tampered run ID should be rejected."
        $script:testsRun++
    }
    finally {
        Remove-Item -LiteralPath $runPath -Recurse -Force
    }
}

function Test-RealisticNodeFixtureFlow {
    $repoPath = Join-Path $fixturesRoot "realistic-node-app"
    $runPath = New-RunDirectory
    try {
        $profileResult = Invoke-Script -ScriptName "resolve-stack-profile.ps1" -Arguments @("-RepoPath", $repoPath)
        Assert-True ($profileResult.ExitCode -eq 0) "Realistic Node fixture detection should succeed."
        $profile = $profileResult.Output | ConvertFrom-Json
        Assert-True ($profile.name -eq "node") "Expected node profile."
        Assert-True ($profile.lintCommand -eq "npm run lint") "Expected lint command for realistic node fixture."

        Initialize-RunArtifacts -RunPath $runPath -RunId "real-node-001" -CurrentStage "test" -TestEvidence $profile.testCommand
        Write-Artifact -RunPath $runPath -Name "task-ledger.md" -Content "Run ID: real-node-001`nCurrent Stage: test`nOwner: planner | Files: docs/plan.md`nOwner: coder | Files: src/app.ts, tests/app.test.ts"
        $transitionResult = Invoke-Script -ScriptName "validate-stage.ps1" -Arguments @("-RunPath", $runPath, "-CurrentStage", "test", "-TargetStage", "review")
        Assert-True ($transitionResult.ExitCode -eq 0) "Realistic Node fixture review transition should pass."
        $script:testsRun++
    }
    finally {
        Remove-Item -LiteralPath $runPath -Recurse -Force
    }
}

function Test-RealisticPythonFixtureFlow {
    $repoPath = Join-Path $fixturesRoot "realistic-python-app"
    $runPath = New-RunDirectory
    try {
        $profileResult = Invoke-Script -ScriptName "resolve-stack-profile.ps1" -Arguments @("-RepoPath", $repoPath)
        Assert-True ($profileResult.ExitCode -eq 0) "Realistic Python fixture detection should succeed."
        $profile = $profileResult.Output | ConvertFrom-Json
        Assert-True ($profile.name -eq "python") "Expected python profile."
        Assert-True ($profile.testCommand -eq "pytest") "Expected pytest command."

        Initialize-RunArtifacts -RunPath $runPath -RunId "real-python-001" -CurrentStage "review" -TestEvidence $profile.testCommand
        Write-Artifact -RunPath $runPath -Name "approval-note.md" -Content "Run ID: real-python-001`nApproved by: reviewer"
        $transitionResult = Invoke-Script -ScriptName "validate-stage.ps1" -Arguments @("-RunPath", $runPath, "-CurrentStage", "review", "-TargetStage", "done", "-RequireApproval")
        Assert-True ($transitionResult.ExitCode -eq 0) "Realistic Python fixture completion should pass."
        $script:testsRun++
    }
    finally {
        Remove-Item -LiteralPath $runPath -Recurse -Force
    }
}

function Test-PromptInjectionFixtureStillRequiresGates {
    $repoPath = Join-Path $fixturesRoot "prompt-injection-app"
    $runPath = New-RunDirectory
    try {
        $profileResult = Invoke-Script -ScriptName "resolve-stack-profile.ps1" -Arguments @("-RepoPath", $repoPath)
        Assert-True ($profileResult.ExitCode -eq 0) "Prompt injection fixture detection should succeed."
        $profile = $profileResult.Output | ConvertFrom-Json
        Assert-True ($profile.name -eq "node") "Expected node profile."

        Write-RunMetadata -RunPath $runPath -RunId "inject-001"
        Write-Artifact -RunPath $runPath -Name "plan.md" -Content "Run ID: inject-001`nPlan"
        Write-Artifact -RunPath $runPath -Name "task-ledger.md" -Content "Run ID: inject-001`nCurrent Stage: test`nOwner: planner | Files: docs/plan.md`nOwner: coder | Files: src/app.ts"
        Write-Artifact -RunPath $runPath -Name "build-log.md" -Content "Run ID: inject-001`nBuild"
        Write-Artifact -RunPath $runPath -Name "test-report.md" -Content "Run ID: inject-001`nRESULT: PASS"

        $transitionResult = Invoke-Script -ScriptName "validate-stage.ps1" -Arguments @("-RunPath", $runPath, "-CurrentStage", "test", "-TargetStage", "review")
        Assert-True ($transitionResult.ExitCode -ne 0) "Prompt injection fixture should still require evidence and gates."
        $script:testsRun++
    }
    finally {
        Remove-Item -LiteralPath $runPath -Recurse -Force
    }
}

function Test-EndToEndRejectsOwnershipConflict {
    $repoPath = Join-Path $fixturesRoot "node-app"
    $runPath = New-RunDirectory
    try {
        $profileResult = Invoke-Script -ScriptName "resolve-stack-profile.ps1" -Arguments @("-RepoPath", $repoPath)
        Assert-True ($profileResult.ExitCode -eq 0) "Node fixture detection should succeed."
        $profile = $profileResult.Output | ConvertFrom-Json

        Initialize-RunArtifacts -RunPath $runPath -RunId "ownership-e2e-001" -CurrentStage "test" -TestEvidence $profile.testCommand
        Write-Artifact -RunPath $runPath -Name "task-ledger.md" -Content "Run ID: ownership-e2e-001`nCurrent Stage: test`nOwner: planner | Files: docs/plan.md, src/app.ts`nOwner: coder | Files: src/app.ts"
        $transitionResult = Invoke-Script -ScriptName "validate-stage.ps1" -Arguments @("-RunPath", $runPath, "-CurrentStage", "test", "-TargetStage", "review")
        Assert-True ($transitionResult.ExitCode -ne 0) "Ownership conflict should be rejected end to end."
        $script:testsRun++
    }
    finally {
        Remove-Item -LiteralPath $runPath -Recurse -Force
    }
}

Test-NodeFixtureEndToEnd
Test-PythonFixtureEndToEnd
Test-UnsupportedFixtureFailsClosed
Test-EndToEndRejectsRunIdTamper
Test-EndToEndRejectsOwnershipConflict
Test-RealisticNodeFixtureFlow
Test-RealisticPythonFixtureFlow
Test-PromptInjectionFixtureStillRequiresGates

Write-Host "Orchex E2E tests passed: $testsRun"
