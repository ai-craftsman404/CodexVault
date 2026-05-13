param(
    [string]$Path = (Get-Location).Path
)

. "$PSScriptRoot/lib/codexvault-shared.ps1"

$workspacePath = (Resolve-Path $Path).Path
$osDescription = [System.Runtime.InteropServices.RuntimeInformation]::OSDescription
$platform = if ($osDescription -match 'Windows') { 'Windows' } elseif ($osDescription -match 'Linux') { 'Linux' } elseif ($osDescription -match 'Darwin|macOS' -or $osDescription -match 'OSX') { 'macOS' } else { 'Unknown' }
$gitRoot = $null
$gitBranch = $null
$gitCommit = $null
try {
    if (Get-Command git -ErrorAction SilentlyContinue) {
        $inside = & git -C $workspacePath rev-parse --is-inside-work-tree 2>$null
        if ($inside -and $inside.Trim() -eq 'true') {
            $gitRoot = (& git -C $workspacePath rev-parse --show-toplevel 2>$null).Trim()
            $gitBranch = (& git -C $workspacePath branch --show-current 2>$null).Trim()
            $gitCommit = (& git -C $workspacePath rev-parse HEAD 2>$null).Trim()
        }
    }
} catch {}

$toolchain = [ordered]@{
    git = Get-CvxCommandVersion -Name 'git'
    npm = Get-CvxCommandVersion -Name 'npm'
    node = Get-CvxCommandVersion -Name 'node'
    python = Get-CvxCommandVersion -Name 'python'
    pwsh = $PSVersionTable.PSVersion.ToString()
    bash = if ($PSVersionTable.PSEdition -eq 'Core' -and $PSVersionTable.OS -and ($PSVersionTable.OS -match 'Linux|Darwin')) { Get-CvxCommandVersion -Name 'bash' } else { $null }
}

$result = [pscustomobject]@{
    timestamp = New-CvxTimestamp
    workspacePath = $workspacePath
    os = $platform
    shell = if ($PSVersionTable.PSVersion) { 'PowerShell' } else { 'Unknown' }
    git = [ordered]@{
        root = $gitRoot
        branch = $gitBranch
        commit = $gitCommit
    }
    toolchain = $toolchain
    packageManagers = @(
        if (Get-Command npm -ErrorAction SilentlyContinue) { 'npm' }
        if (Get-Command python -ErrorAction SilentlyContinue) { 'python' }
    )
    codexPaths = @($workspacePath)
    status = 'discovered'
    summary = 'Workspace discovery complete'
}

$result | ConvertTo-Json -Depth 6
