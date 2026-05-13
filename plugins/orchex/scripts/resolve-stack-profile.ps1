[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)]
    [string]$RepoPath,

    [string]$ProfilePath
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function New-ProfileObject {
    param(
        [string]$Name,
        [bool]$Supported,
        [string[]]$DetectedFiles,
        [string]$TestCommand = "",
        [string]$BuildCommand = "",
        [string]$LintCommand = "",
        [string]$Notes = ""
    )

    [pscustomobject]@{
        name          = $Name
        supported     = $Supported
        detectedFiles = $DetectedFiles
        testCommand   = $TestCommand
        buildCommand  = $BuildCommand
        lintCommand   = $LintCommand
        notes         = $Notes
    }
}

$resolvedRepoPath = (Resolve-Path -LiteralPath $RepoPath).Path

if ($ProfilePath) {
    $resolvedProfilePath = (Resolve-Path -LiteralPath $ProfilePath).Path
    Get-Content -LiteralPath $resolvedProfilePath -Raw | ConvertFrom-Json | ConvertTo-Json -Depth 6
    exit 0
}

$packageJsonPath = Join-Path $resolvedRepoPath "package.json"
$pyprojectPath = Join-Path $resolvedRepoPath "pyproject.toml"
$requirementsPath = Join-Path $resolvedRepoPath "requirements.txt"
$cargoTomlPath = Join-Path $resolvedRepoPath "Cargo.toml"
$solutionPath = Get-ChildItem -LiteralPath $resolvedRepoPath -Filter *.sln -File -ErrorAction SilentlyContinue | Select-Object -First 1
$projectPath = Get-ChildItem -LiteralPath $resolvedRepoPath -Filter *.csproj -File -Recurse -ErrorAction SilentlyContinue | Select-Object -First 1

if (Test-Path -LiteralPath $packageJsonPath) {
    $package = Get-Content -LiteralPath $packageJsonPath -Raw | ConvertFrom-Json
    $scripts = if ($package.PSObject.Properties.Name -contains "scripts") { $package.scripts } else { $null }
    $profile = New-ProfileObject `
        -Name "node" `
        -Supported $true `
        -DetectedFiles @("package.json") `
        -TestCommand $(if ($scripts -and $scripts.PSObject.Properties.Name -contains "test") { "npm test" } else { "" }) `
        -BuildCommand $(if ($scripts -and $scripts.PSObject.Properties.Name -contains "build") { "npm run build" } else { "" }) `
        -LintCommand $(if ($scripts -and $scripts.PSObject.Properties.Name -contains "lint") { "npm run lint" } else { "" }) `
        -Notes "Detected Node project from package.json."
    $profile | ConvertTo-Json -Depth 6
    exit 0
}

if ((Test-Path -LiteralPath $pyprojectPath) -or (Test-Path -LiteralPath $requirementsPath)) {
    $detected = @()
    if (Test-Path -LiteralPath $pyprojectPath) { $detected += "pyproject.toml" }
    if (Test-Path -LiteralPath $requirementsPath) { $detected += "requirements.txt" }
    $profile = New-ProfileObject `
        -Name "python" `
        -Supported $true `
        -DetectedFiles $detected `
        -TestCommand "pytest" `
        -BuildCommand "" `
        -LintCommand "" `
        -Notes "Detected Python project."
    $profile | ConvertTo-Json -Depth 6
    exit 0
}

if (Test-Path -LiteralPath $cargoTomlPath) {
    $profile = New-ProfileObject `
        -Name "rust" `
        -Supported $true `
        -DetectedFiles @("Cargo.toml") `
        -TestCommand "cargo test" `
        -BuildCommand "cargo build" `
        -LintCommand "cargo fmt --check" `
        -Notes "Detected Rust project."
    $profile | ConvertTo-Json -Depth 6
    exit 0
}

if ($solutionPath -or $projectPath) {
    $detected = @()
    if ($solutionPath) { $detected += $solutionPath.Name }
    if ($projectPath) { $detected += $projectPath.Name }
    $profile = New-ProfileObject `
        -Name "dotnet" `
        -Supported $true `
        -DetectedFiles $detected `
        -TestCommand "dotnet test" `
        -BuildCommand "dotnet build" `
        -LintCommand "" `
        -Notes "Detected .NET project."
    $profile | ConvertTo-Json -Depth 6
    exit 0
}

$unsupported = New-ProfileObject `
    -Name "unknown" `
    -Supported $false `
    -DetectedFiles @() `
    -Notes "No supported stack profile was detected. Provide an explicit profile configuration."

$unsupported | ConvertTo-Json -Depth 6
