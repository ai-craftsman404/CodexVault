param(
    [Parameter(Mandatory=$true)][string]$ScenarioJson
)

. "$PSScriptRoot/lib/codexvault-shared.ps1"

$scenario = $ScenarioJson | ConvertFrom-Json
$paths = Get-CvxPathConfig -WorkspacePath $scenario.workspacePath
$simulation = [pscustomobject]@{
    schemaVersion = 'v1a'
    status = 'simulation complete'
    headline = 'Agent-team simulation complete'
    adjudication = [ordered]@{
        claims = @('restore plan is structurally valid')
        supportingEvidence = @('manifest shape matches expected contract')
        disputesResolved = @('temporary restore scope remains isolated')
        decision = 'proceed-with-warnings'
        confidenceDelta = 0.1
    }
    findings = @(
        'discovery agent identified workspace scope',
        'snapshot agent confirmed manifest completeness placeholder',
        'restore planning agent requested approval checkpoint'
    )
}

$simulationTempRoot = Join-Path $paths.simulationDir 'temp'
$simulationPath = $null
$cleanupStatus = 'not-started'

try {
    if (-not (Test-Path -LiteralPath $paths.simulationDir)) {
        New-Item -ItemType Directory -Path $paths.simulationDir -Force | Out-Null
    }
    if (Test-Path -LiteralPath $simulationTempRoot) {
        Remove-Item -LiteralPath $simulationTempRoot -Recurse -Force
    }
    New-Item -ItemType Directory -Path $simulationTempRoot -Force | Out-Null
    $simulationPath = Join-Path $simulationTempRoot "simulation-$((Get-Date).ToString('yyyyMMddTHHmmssZ')).json"
    ($simulation | ConvertTo-Json -Depth 6) | Set-Content -LiteralPath $simulationPath -Encoding UTF8
    $cleanupStatus = 'pending'
} catch {
    $cleanupStatus = 'failed'
    throw
} finally {
    if (Test-Path -LiteralPath $simulationTempRoot) {
        Remove-Item -LiteralPath $simulationTempRoot -Recurse -Force
        $cleanupStatus = 'cleaned'
    }
}

[pscustomobject]@{
    simulationPath = $simulationPath
    cleanupStatus = $cleanupStatus
    adjudication = $simulation.adjudication
    simulation = $simulation
} | ConvertTo-Json -Depth 6
