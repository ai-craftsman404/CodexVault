param(
    [Parameter(Mandatory=$true)][string]$ScenarioJson
)

. "$PSScriptRoot/lib/codexvault-shared.ps1"

$simulation = [pscustomobject]@{
    schemaVersion = 'v1a'
    status = 'simulation complete'
    headline = 'Agent-team simulation stub'
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

$scenario = $ScenarioJson | ConvertFrom-Json
$paths = Get-CvxPathConfig -WorkspacePath $scenario.workspacePath
if (-not (Test-Path -LiteralPath $paths.simulationDir)) {
    New-Item -ItemType Directory -Path $paths.simulationDir -Force | Out-Null
}
$simulationPath = Join-Path $paths.simulationDir "simulation-$((Get-Date).ToString('yyyyMMddTHHmmssZ')).json"
($simulation | ConvertTo-Json -Depth 6) | Set-Content -LiteralPath $simulationPath -Encoding UTF8

[pscustomobject]@{
    simulationPath = $simulationPath
    adjudication = $simulation.adjudication
    simulation = $simulation
} | ConvertTo-Json -Depth 6
