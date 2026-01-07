# EduPath Optimizer - Quick Deployment Script
# Deploys to Render.com (Free Tier)

Write-Host "================================" -ForegroundColor Cyan
Write-Host "  EduPath Optimizer Deployment" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# Check if git is initialized
if (!(Test-Path ".git")) {
    Write-Host "[1/6] Initializing Git repository..." -ForegroundColor Yellow
    git init
    git add .
    git commit -m "Initial commit - Production ready"
} else {
    Write-Host "[1/6] Git repository exists" -ForegroundColor Green
}

# Check for uncommitted changes
$status = git status --porcelain
if ($status) {
    Write-Host "[2/6] Committing changes..." -ForegroundColor Yellow
    git add .
    git commit -m "Deploy: $(Get-Date -Format 'yyyy-MM-dd HH:mm')"
} else {
    Write-Host "[2/6] No changes to commit" -ForegroundColor Green
}

# Check if remote exists
$remotes = git remote
if ($remotes -notcontains "origin") {
    Write-Host ""
    Write-Host "[3/6] GitHub repository not connected" -ForegroundColor Yellow
    Write-Host "Please create a GitHub repository and run:" -ForegroundColor White
    Write-Host "  git remote add origin https://github.com/YOUR_USERNAME/edupath-optimizer.git" -ForegroundColor Cyan
    Write-Host "  git push -u origin main" -ForegroundColor Cyan
    Write-Host ""
    $continue = Read-Host "Have you set up GitHub? (y/n)"
    if ($continue -ne "y") {
        Write-Host "Deployment cancelled. Set up GitHub first." -ForegroundColor Red
        exit
    }
} else {
    Write-Host "[3/6] GitHub remote configured" -ForegroundColor Green
}

# Push to GitHub
Write-Host "[4/6] Pushing to GitHub..." -ForegroundColor Yellow
try {
    git push origin main
    Write-Host "Successfully pushed to GitHub!" -ForegroundColor Green
} catch {
    Write-Host "Failed to push. Make sure you're authenticated." -ForegroundColor Red
    Write-Host "Run: gh auth login" -ForegroundColor Cyan
    exit
}

Write-Host ""
Write-Host "[5/6] Opening Render.com deployment page..." -ForegroundColor Yellow
Start-Sleep -Seconds 2
start "https://render.com/deploy"

Write-Host ""
Write-Host "================================" -ForegroundColor Green
Write-Host "  Next Steps on Render.com:" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Green
Write-Host ""
Write-Host "1. Click 'New' → 'Web Service'" -ForegroundColor White
Write-Host "2. Connect your GitHub repository" -ForegroundColor White
Write-Host "3. Configure:" -ForegroundColor White
Write-Host "   - Name: edupath-optimizer" -ForegroundColor Cyan
Write-Host "   - Region: Oregon (US West)" -ForegroundColor Cyan
Write-Host "   - Branch: main" -ForegroundColor Cyan
Write-Host "   - Root Directory: (leave blank)" -ForegroundColor Cyan
Write-Host "   - Runtime: Python 3" -ForegroundColor Cyan
Write-Host "   - Build Command:" -ForegroundColor Cyan
Write-Host "     pip install -r backend/requirements.txt && python backend/train_model.py" -ForegroundColor Yellow
Write-Host "   - Start Command:" -ForegroundColor Cyan
Write-Host "     cd backend && python app.py" -ForegroundColor Yellow
Write-Host ""
Write-Host "4. Add Environment Variables (Advanced → Environment):" -ForegroundColor White
Write-Host "   - FLASK_ENV=production" -ForegroundColor Cyan
Write-Host "   - PORT=10000" -ForegroundColor Cyan
Write-Host "   - FLASK_DEBUG=False" -ForegroundColor Cyan
Write-Host "   - Copy other variables from .env file" -ForegroundColor Cyan
Write-Host ""
Write-Host "5. Click 'Create Web Service'" -ForegroundColor White
Write-Host ""
Write-Host "[6/6] Waiting for your deployment..." -ForegroundColor Yellow
Write-Host "This will take 3-5 minutes. Your live link will be:" -ForegroundColor White
Write-Host "https://edupath-optimizer.onrender.com" -ForegroundColor Green
Write-Host ""
Write-Host "Press any key once deployed to test..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown')

Write-Host ""
Write-Host "Testing deployment..." -ForegroundColor Yellow
$url = Read-Host "Enter your Render URL (e.g., https://edupath-optimizer.onrender.com)"

try {
    $health = Invoke-RestMethod -Uri "$url/api/health" -Method Get
    Write-Host ""
    Write-Host "✅ SUCCESS! Your app is live!" -ForegroundColor Green
    Write-Host "Health Check: $($health | ConvertTo-Json)" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "🎉 Share your live link:" -ForegroundColor Green
    Write-Host "$url/frontend/auth/login.html" -ForegroundColor Cyan
    Write-Host ""
    start "$url/frontend/auth/login.html"
} catch {
    Write-Host "⚠️ Deployment still in progress or failed" -ForegroundColor Yellow
    Write-Host "Check Render dashboard for logs" -ForegroundColor White
}

Write-Host ""
Write-Host "================================" -ForegroundColor Green
Write-Host "Deployment Complete!" -ForegroundColor Green
Write-Host "================================" -ForegroundColor Green
