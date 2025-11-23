# Installation Script for AI Meeting Summarizer
# Run this to set up your environment

Write-Host "🎯 AI Meeting Summarizer - Installation Script" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Check Python installation
Write-Host "1️⃣ Checking Python installation..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version 2>&1
    Write-Host "   ✅ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "   ❌ Python not found! Please install Python 3.8+ first" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "2️⃣ Installing dependencies..." -ForegroundColor Yellow
pip install streamlit pillow pandas numpy python-dotenv

Write-Host ""
Write-Host "3️⃣ Checking installation..." -ForegroundColor Yellow
$streamlitVersion = streamlit --version 2>&1
Write-Host "   ✅ Streamlit installed: $streamlitVersion" -ForegroundColor Green

Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "✨ Installation Complete!" -ForegroundColor Green
Write-Host ""
Write-Host "To run the application:" -ForegroundColor Cyan
Write-Host "   streamlit run src/app_ui.py" -ForegroundColor White
Write-Host ""
Write-Host "Or use the run script:" -ForegroundColor Cyan
Write-Host "   .\run_app.ps1" -ForegroundColor White
Write-Host ""
Write-Host "📚 Check SETUP_COMPLETE.md for next steps!" -ForegroundColor Yellow
Write-Host ""
