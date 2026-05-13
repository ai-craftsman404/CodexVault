Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

function New-CvxTimestamp {
    Get-Date -Format 'yyyyMMddTHHmmssZ'
}

function New-CvxErrorRecord {
    param(
        [Parameter(Mandatory=$true)][string]$Code,
        [Parameter(Mandatory=$true)][string]$Message,
        [string]$Detail = ''
    )

    [pscustomobject]@{
        code = $Code
        message = $Message
        detail = $Detail
    }
}

function New-CvxHighlight {
    param(
        [Parameter(Mandatory=$true)][string]$Headline,
        [Parameter(Mandatory=$true)][string]$Status,
        [string]$Detail = '',
        [string]$Action = ''
    )

    [pscustomobject]@{
        headline = $Headline
        status = $Status
        detail = $Detail
        action = $Action
    }
}

function New-CvxSha256 {
    param(
        [Parameter(Mandatory=$true)][string]$Text
    )

    $bytes = [System.Text.Encoding]::UTF8.GetBytes($Text)
    $sha = [System.Security.Cryptography.SHA256]::Create()
    try {
        ($sha.ComputeHash($bytes) | ForEach-Object { $_.ToString('x2') }) -join ''
    } finally {
        $sha.Dispose()
    }
}

function New-CvxSha256File {
    param(
        [Parameter(Mandatory=$true)][string]$Path
    )

    $sha = [System.Security.Cryptography.SHA256]::Create()
    try {
        $stream = [System.IO.File]::OpenRead($Path)
        try {
            ($sha.ComputeHash($stream) | ForEach-Object { $_.ToString('x2') }) -join ''
        } finally {
            $stream.Dispose()
        }
    } finally {
        $sha.Dispose()
    }
}

function New-CvxStableGuid {
    param(
        [Parameter(Mandatory=$true)][string]$Seed
    )

    $hash = New-CvxSha256 -Text $Seed
    $hex = $hash.Substring(0, 32)
    [guid]::ParseExact($hex, 'N')
}

function Get-CvxCommandVersion {
    param(
        [Parameter(Mandatory=$true)][string]$Name
    )

    $cmd = Get-Command $Name -ErrorAction SilentlyContinue
    if (-not $cmd) { return $null }

    try {
        if ($cmd.Source -and ($cmd.Source -match '\.exe$|\.bat$|\.cmd$')) {
            return (& $Name --version 2>$null | Select-Object -First 1)
        }
        if ($cmd.Name -eq 'git') {
            return (& $Name --version 2>$null | Select-Object -First 1)
        }
    } catch {
        return $null
    }

    return $cmd.Source
}

function Get-CvxWorkspaceFiles {
    param(
        [Parameter(Mandatory=$true)][string]$WorkspacePath
    )

    if (-not (Test-Path -LiteralPath $WorkspacePath)) {
        return @()
    }

    $excludeNames = @('.git', '.svn', '.hg', 'node_modules', '__pycache__', '.codexvault', '.DS_Store')
    Get-ChildItem -LiteralPath $WorkspacePath -Recurse -File -Force | Where-Object {
        $parts = $_.FullName.Substring($WorkspacePath.Length).TrimStart('\','/')
        if (-not $parts) { return $false }
        foreach ($name in $excludeNames) {
            if ($_.FullName -match [regex]::Escape([IO.Path]::DirectorySeparatorChar + $name) -or $_.Name -eq $name) {
                return $false
            }
        }
        return $true
    }
}

function Get-CvxPathConfig {
    param(
        [Parameter(Mandatory=$true)][string]$WorkspacePath
    )

    $root = [System.IO.Path]::GetFullPath($WorkspacePath)
    $cvxRoot = Join-Path $root '.codexvault'
    [pscustomobject]@{
        workspaceRoot = $root
        backupDestinationDir = Join-Path $cvxRoot 'snapshots'
        snapshotStagingDir = Join-Path $cvxRoot 'staging'
        manifestOutputDir = Join-Path $cvxRoot 'manifests'
        restorePlanDir = Join-Path $cvxRoot 'restores'
        verificationDir = Join-Path $cvxRoot 'verification'
        simulationDir = Join-Path $cvxRoot 'simulations'
        fixtureRoot = Join-Path $root 'plugins\codexvault\tests\fixtures'
    }
}
