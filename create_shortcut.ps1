<#
Creates a Desktop shortcut to launch the chat bot without using absolute paths.
Targets the batch file in the same directory as this script.
#>

$desktopPath = [Environment]::GetFolderPath('Desktop')
$shortcutPath = Join-Path $desktopPath "ChatBot.lnk"

# Resolve repo root as the folder containing this script
$repoRoot = $PSScriptRoot
$targetPath = Join-Path $repoRoot "launch_chatbot.bat"

$wshShell = New-Object -ComObject WScript.Shell
$shortcut = $wshShell.CreateShortcut($shortcutPath)
$shortcut.TargetPath = $targetPath
$shortcut.WorkingDirectory = $repoRoot
$shortcut.WindowStyle = 1
$shortcut.Description = "Launch ChatGPT Chat Bot"
$shortcut.Save()

Write-Host "Desktop shortcut created successfully at $shortcutPath"