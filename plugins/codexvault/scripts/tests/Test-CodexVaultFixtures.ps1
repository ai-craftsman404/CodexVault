Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$root = Resolve-Path (Join-Path $PSScriptRoot '..\..')
$fixtures = Join-Path $root 'tests\fixtures'

function Read-JsonFile {
    param([Parameter(Mandatory=$true)][string]$Path)
    Get-Content $Path -Raw | ConvertFrom-Json
}

function Assert-Equal {
    param(
        [Parameter(Mandatory=$true)]$Actual,
        [Parameter(Mandatory=$true)]$Expected,
        [Parameter(Mandatory=$true)][string]$Label
    )

    if ($Actual -ne $Expected) {
        throw "$Label mismatch. Expected '$Expected' but got '$Actual'"
    }
}

$windowsDiscovery = Read-JsonFile (Join-Path $fixtures 'windows\discovery.json')
$linuxDiscovery = Read-JsonFile (Join-Path $fixtures 'linux\discovery.json')
$manifestExpected = Read-JsonFile (Join-Path $fixtures 'manifest\expected-v1a.json')
$restoreExpected = Read-JsonFile (Join-Path $fixtures 'restore\expected-plan.json')
$verifyExpected = Read-JsonFile (Join-Path $fixtures 'verify\expected-report.json')
$simulationExpected = Read-JsonFile (Join-Path $fixtures 'simulation\expected-adjudication.json')
$invalidManifest = Read-JsonFile (Join-Path $fixtures 'negative\invalid-manifest.json')
$malformedManifest = Get-Content (Join-Path $fixtures 'negative\malformed-json-manifest.json') -Raw
$missingCheckpointsPlan = Read-JsonFile (Join-Path $fixtures 'negative\missing-checkpoints-plan.json')
$badChecksumSidecar = Read-JsonFile (Join-Path $fixtures 'negative\bad-checksum-sidecar.json')
$pathTraversalEntry = Get-Content (Join-Path $fixtures 'negative\path-traversal-entry.txt') -Raw

Assert-Equal -Actual $windowsDiscovery.status -Expected 'discovered' -Label 'Windows discovery status'
Assert-Equal -Actual $linuxDiscovery.status -Expected 'discovered' -Label 'Linux discovery status'
Assert-Equal -Actual $manifestExpected.schemaVersion -Expected 'v1a' -Label 'Manifest schemaVersion'
Assert-Equal -Actual $restoreExpected.approvalRequired -Expected $true -Label 'Restore approvalRequired'
Assert-Equal -Actual $verifyExpected.validationStatus -Expected 'validated-with-warnings' -Label 'Verification status'
Assert-Equal -Actual $simulationExpected.status -Expected 'simulation complete' -Label 'Simulation status'
Assert-Equal -Actual $invalidManifest.workspaceId -Expected '' -Label 'Invalid manifest workspaceId'
if ($malformedManifest -notmatch ',\s*}') { throw 'Malformed manifest fixture did not preserve trailing comma corruption' }
if ($missingCheckpointsPlan.PSObject.Properties.Name -contains 'checkpoints') { throw 'Missing checkpoints plan unexpectedly included checkpoints' }
Assert-Equal -Actual $badChecksumSidecar.checksum -Expected 'deadbeef' -Label 'Bad checksum sidecar'
if ($pathTraversalEntry -notmatch '\.\./escape\.txt') { throw 'Path traversal entry fixture missing expected traversal path' }

$liveDiscovery = & "$root\scripts\discover_workspace.ps1" -Path (Resolve-Path (Join-Path $root '..\..')).Path
$manifestJson = & "$root\scripts\write_manifest.ps1" -DiscoveryJson $liveDiscovery
$manifestEnvelope = $manifestJson | ConvertFrom-Json
$manifest = $manifestEnvelope.manifest
Assert-Equal -Actual $manifest.schemaVersion -Expected 'v1a' -Label 'Generated manifest schemaVersion'
if ([string]::IsNullOrWhiteSpace($manifest.workspaceId)) { throw 'Generated manifest workspaceId was empty' }

$snapshotJson = & "$root\scripts\create_snapshot.ps1" -ManifestJson (($manifest | ConvertTo-Json -Depth 8).Trim())
$snapshot = $snapshotJson | ConvertFrom-Json
Assert-Equal -Actual $snapshot.checksumAlgorithm -Expected 'SHA-256' -Label 'Snapshot checksum algorithm'
if ([string]::IsNullOrWhiteSpace($snapshot.checksum)) { throw 'Snapshot checksum was empty' }

$planJson = & "$root\scripts\plan_restore.ps1" -ManifestJson (($manifest | ConvertTo-Json -Depth 8).Trim())
$planEnvelope = $planJson | ConvertFrom-Json
$reportJson = & "$root\scripts\verify_restore.ps1" -PlanJson (($planEnvelope.plan | ConvertTo-Json -Depth 6).Trim())
$reportEnvelope = $reportJson | ConvertFrom-Json
$report = $reportEnvelope.report
Assert-Equal -Actual $report.validationStatus -Expected 'validated' -Label 'Verification validationStatus'

$simulationJson = & "$root\scripts\simulate_restore_team.ps1" -ScenarioJson (@{ workspacePath = (Resolve-Path (Join-Path $root '..\..')).Path } | ConvertTo-Json)
$simulationEnvelope = $simulationJson | ConvertFrom-Json
if (-not $simulationEnvelope.adjudication) { throw 'Simulation adjudication envelope missing' }
Assert-Equal -Actual $simulationEnvelope.cleanupStatus -Expected 'cleaned' -Label 'Simulation cleanupStatus'

Write-Output 'CodexVault fixture tests passed.'
