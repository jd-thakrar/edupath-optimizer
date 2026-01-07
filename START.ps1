# EduPath Optimizer - Quick Start Script
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  EduPath Optimizer - Starting...  " -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

# Start Backend in new window
Write-Host "`n[1/2] Starting Backend Server..." -ForegroundColor Yellow
Start-Process cmd -ArgumentList "/k", "cd /d C:\Users\JEET\Downloads\EDU && C:/Users/JEET/Downloads/EDU/.venv-1/Scripts/python.exe backend/app.py"
Start-Sleep -Seconds 5

# Test backend
Write-Host "[2/2] Testing Backend..." -ForegroundColor Yellow
try {
    $response = Invoke-RestMethod -Uri "http://localhost:5000/api/health" -Method GET
    Write-Host "Backend is running!" -ForegroundColor Green
    Write-Host "  - Model Loaded: $($response.model_loaded)" -ForegroundColor White
    Write-Host "  - Port: 5000" -ForegroundColor White
} catch {
    Write-Host "Backend failed to start!" -ForegroundColor Red
    exit 1
}

# Open Dashboard
Write-Host "`nOpening Dashboard..." -ForegroundColor Yellow
Start-Sleep -Seconds 1
start frontend\student\dashboard.html

Write-Host "`n========================================" -ForegroundColor Green
Write-Host "  System Ready!" -ForegroundColor Green  
Write-Host "========================================" -ForegroundColor Green
Write-Host "`nBackend: http://localhost:5000" -ForegroundColor White
Write-Host "Dashboard: frontend/student/dashboard.html" -ForegroundColor White
Write-Host "Press Ctrl+C in backend window to stop" -ForegroundColor Yellow
