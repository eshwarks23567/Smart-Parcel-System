# Stop any running python app.py processes for this project
Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -and $_.CommandLine -match 'app.py' } | ForEach-Object {
    $p = $_.ProcessId
    Write-Host "Stopping process PID=$p"
    Stop-Process -Id $p -Force -ErrorAction SilentlyContinue
}
Write-Host 'Stopped app.py processes.'
