# Start the Flask app in the background using the virtualenv python
param(
  [string]$VenvPath = ".venv\Scripts\python.exe",
  [string]$App = "app.py"
)

if (-not (Test-Path $VenvPath)) {
  Write-Error "Python executable not found at $VenvPath"
  exit 1
}

Start-Process -NoNewWindow -FilePath $VenvPath -ArgumentList $App
Write-Host "Started $App using $VenvPath"
