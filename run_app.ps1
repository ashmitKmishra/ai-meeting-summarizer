# Run Script for AI Meeting Summarizer

Write-Host "🚀 Starting AI Meeting Summarizer..." -ForegroundColor Cyan
Write-Host ""

# Check if streamlit is installed
try {
    streamlit --version | Out-Null
    Write-Host "✅ Streamlit found" -ForegroundColor Green
} catch {
    Write-Host "❌ Streamlit not found! Please run install.ps1 first" -ForegroundColor Red
    Write-Host ""
    Write-Host "Run: .\install.ps1" -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "Opening application..." -ForegroundColor Yellow
Write-Host "The app will be available at: http://localhost:8501" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Ctrl+C to stop the server" -ForegroundColor Gray
Write-Host ""

streamlit run src/app_ui.py
