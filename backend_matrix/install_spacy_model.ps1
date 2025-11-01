# Quick Fix for NLP Model Installation

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Installing spaCy NLP Model" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

Write-Host "Installing en_core_web_sm model..." -ForegroundColor Yellow
Write-Host "This may take a few minutes...`n" -ForegroundColor Yellow

# Try to install the spaCy model
python -m spacy download en_core_web_sm

if ($LASTEXITCODE -eq 0) {
    Write-Host "`n========================================" -ForegroundColor Green
    Write-Host "Installation Successful!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "`nYou can now use the NLP analysis endpoint." -ForegroundColor Green
    Write-Host "Start the server with: .\start.ps1" -ForegroundColor Green
} else {
    Write-Host "`n========================================" -ForegroundColor Red
    Write-Host "Installation Failed" -ForegroundColor Red
    Write-Host "========================================" -ForegroundColor Red
    Write-Host "`nTrying alternative method..." -ForegroundColor Yellow
    
    # Try alternative installation
    python -m pip install "https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.7.0/en_core_web_sm-3.7.0-py3-none-any.whl"
    
    if ($LASTEXITCODE -eq 0) {
        Write-Host "`n✓ Installation successful!" -ForegroundColor Green
    } else {
        Write-Host "`n✗ Installation failed. Please check your internet connection." -ForegroundColor Red
    }
}

Write-Host "`nPress any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
