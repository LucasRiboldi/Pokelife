param(
    [string]$Executable = (Join-Path $PSScriptRoot '../src/TaskbarHabitat.Widget/bin/Release/net10.0-windows10.0.26100.0/win-x64/TaskbarHabitat.Widget.exe')
)

# Run in an interactive Windows session with other PokeLife instances closed.
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName UIAutomationClient,UIAutomationTypes
Add-Type @"
using System;
using System.Runtime.InteropServices;
public static class TestWindow {
    [DllImport("user32.dll")] public static extern bool ShowWindowAsync(IntPtr hwnd, int command);
    [DllImport("user32.dll")] public static extern bool IsIconic(IntPtr hwnd);
    [DllImport("user32.dll")] public static extern uint GetDpiForWindow(IntPtr hwnd);
}
"@
$exe = (Resolve-Path -LiteralPath $Executable).Path
if (Get-Process -Name ([IO.Path]::GetFileNameWithoutExtension($exe)) -ErrorAction SilentlyContinue) {
    throw 'Close PokeLife before running the smoke test.'
}
$save = Join-Path ([IO.Path]::GetTempPath()) ('PokeLife-Smoke-' + [guid]::NewGuid())
$owned = [Collections.Generic.List[Diagnostics.Process]]::new()
function Launch {
    $start = [Diagnostics.ProcessStartInfo]::new($exe)
    $start.UseShellExecute = $false
    $start.Environment['POKELIFE_SAVE_DIRECTORY'] = $save
    $p = [Diagnostics.Process]::Start($start)
    $owned.Add($p)
    $p
}
function WaitFor([string]$description, [scriptblock]$condition) {
    $limit = [Diagnostics.Stopwatch]::StartNew()
    while ($limit.Elapsed.TotalSeconds -lt 12) {
        try { $value = & $condition } catch [System.Runtime.InteropServices.COMException] { $value = $null }
        if ($value) { return $value }
        Start-Sleep -Milliseconds 100
    }
    throw "Timeout: $description"
}
function Window($p, $title) {
    $p.Refresh()
    if ($p.HasExited) { throw "Unexpected exit $($p.Id): $($p.ExitCode)" }
    if ($p.MainWindowTitle -like $title) { $p.MainWindowHandle }
}
try {
    $first = Launch
    $selection = WaitFor 'starter selection' { Window $first '*Escolha seu inicial*' }
    $duplicate = Launch
    if (!$duplicate.WaitForExit(10000) -or $duplicate.ExitCode -ne 0) { throw 'Second launch did not exit cleanly during selection' }
    if ((Window $first '*Escolha seu inicial*') -ne $selection) { throw 'Selection window changed on relaunch' }
    $automation = [Windows.Automation.AutomationElement]::FromHandle($selection)
    $name = [Windows.Automation.PropertyCondition]::new([Windows.Automation.AutomationElement]::NameProperty, 'Charmander')
    $button = WaitFor 'Charmander button' { $automation.FindFirst([Windows.Automation.TreeScope]::Descendants, $name) }
    $button.GetCurrentPattern([Windows.Automation.InvokePattern]::Pattern).Invoke()
    $habitat = WaitFor 'habitat after selection' { Window $first '*Floresta de Viridian*' }
    Write-Output "PID $($first.Id), DPI $([TestWindow]::GetDpiForWindow($habitat)), save $save"
    [TestWindow]::ShowWindowAsync($habitat, 6) | Out-Null
    WaitFor 'habitat minimized' { [TestWindow]::IsIconic($habitat) } | Out-Null
    $second = Launch
    if (!$second.WaitForExit(7000)) {
        throw 'Second launch did not exit'
    }
    if ($second.ExitCode -ne 0) { throw "Second launch exit code $($second.ExitCode)" }
    WaitFor 'same habitat restored' { ![TestWindow]::IsIconic($habitat) } | Out-Null
    if ((Window $first '*Floresta de Viridian*') -ne $habitat) { throw 'Habitat window changed on relaunch' }
    if (!$first.CloseMainWindow() -or !$first.WaitForExit(8000) -or $first.ExitCode -ne 0) { throw 'Habitat close did not exit cleanly' }
    $third = Launch
    WaitFor 'reopen directly in saved habitat' { Window $third '*Floresta de Viridian*' } | Out-Null
    $savedWindow = [Windows.Automation.AutomationElement]::FromHandle($third.MainWindowHandle)
    WaitFor 'Charmander restored from save' {
        $labels = $savedWindow.FindAll([Windows.Automation.TreeScope]::Descendants, [Windows.Automation.Condition]::TrueCondition)
        $labels | Where-Object { $_.Current.Name -like 'Charmander*' } | Select-Object -First 1
    } | Out-Null
    if (!$third.CloseMainWindow() -or !$third.WaitForExit(8000) -or $third.ExitCode -ne 0) { throw 'Reopened habitat did not close cleanly' }
    Write-Output 'PASS: selection, duplicate launches, restore, exit, persisted starter'
} finally {
    foreach ($p in $owned) {
        $p.Refresh()
        if (!$p.HasExited) {
            $p.CloseMainWindow() | Out-Null
            $p.WaitForExit(2500) | Out-Null
        }
        $p.Dispose()
    }
}
