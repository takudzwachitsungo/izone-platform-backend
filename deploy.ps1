# Vercel Deployment Script for iZonehub Backend (PowerShell)

Write-Host "🚀 Preparing iZonehub Backend for Vercel Deployment" -ForegroundColor Green

# Check if Vercel CLI is installed
try {
    vercel --version | Out-Null
    Write-Host "✅ Vercel CLI found" -ForegroundColor Green
} catch {
    Write-Host "❌ Vercel CLI not found. Installing..." -ForegroundColor Red
    npm install -g vercel
}

# Check if we're in the backend directory
if (-not (Test-Path "main.py")) {
    Write-Host "❌ Please run this script from the backend directory" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Backend directory confirmed" -ForegroundColor Green

# Check for required files
if (-not (Test-Path "vercel.json")) {
    Write-Host "❌ vercel.json not found" -ForegroundColor Red
    exit 1
}

if (-not (Test-Path "requirements.txt")) {
    Write-Host "❌ requirements.txt not found" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Required files found" -ForegroundColor Green

# Deploy to Vercel
Write-Host "🌐 Deploying to Vercel..." -ForegroundColor Blue
vercel --prod

Write-Host "🎉 Deployment complete!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Next Steps:" -ForegroundColor Yellow
Write-Host "1. Set up environment variables in Vercel dashboard:"
Write-Host "   - DATABASE_URL (PostgreSQL connection string)"
Write-Host "   - SECRET_KEY (32+ character random string)" 
Write-Host "   - SMTP_PASSWORD (your app password)"
Write-Host ""
Write-Host "2. Update your frontend to use the new API URL"
Write-Host "3. Configure your database on a cloud provider"
Write-Host ""
Write-Host "🔗 Visit your Vercel dashboard to see the deployment URL" -ForegroundColor Cyan