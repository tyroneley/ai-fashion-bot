# PyTorch DLL Error Fix Script for Windows

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "PyTorch DLL Error Fix" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

Write-Host "The error you're seeing is caused by missing Visual C++ Runtime libraries.`n"

Write-Host "SOLUTION 1: Install Visual C++ Redistributables (RECOMMENDED)" -ForegroundColor Green
Write-Host "-----------------------------------------------------------"
Write-Host "1. Download from: " -NoNewline
Write-Host "https://aka.ms/vs/17/release/vc_redist.x64.exe" -ForegroundColor Yellow
Write-Host "2. Run the installer"
Write-Host "3. Restart your terminal and server`n"

Write-Host "SOLUTION 2: Download automatically (requires admin)" -ForegroundColor Green
Write-Host "-----------------------------------------------------------"
$response = Read-Host "Would you like me to download and install it now? (y/n)"

if ($response -eq 'y' -or $response -eq 'Y') {
    Write-Host "`nDownloading Visual C++ Redistributable..." -ForegroundColor Cyan
    $url = "https://aka.ms/vs/17/release/vc_redist.x64.exe"
    $output = "$env:TEMP\vc_redist.x64.exe"
    
    try {
        Invoke-WebRequest -Uri $url -OutFile $output
        Write-Host "Download complete!`n" -ForegroundColor Green
        Write-Host "Installing... (This may require administrator privileges)" -ForegroundColor Yellow
        Start-Process -FilePath $output -ArgumentList "/install", "/quiet", "/norestart" -Wait -Verb RunAs
        Write-Host "`nInstallation complete!" -ForegroundColor Green
        Write-Host "Please restart your terminal and run the server again.`n" -ForegroundColor Yellow
    }
    catch {
        Write-Host "`nError during download/installation: $_" -ForegroundColor Red
        Write-Host "Please download and install manually from: https://aka.ms/vs/17/release/vc_redist.x64.exe`n" -ForegroundColor Yellow
    }
}
else {
    Write-Host "`nPlease install manually from: https://aka.ms/vs/17/release/vc_redist.x64.exe" -ForegroundColor Yellow
    Write-Host "After installation, restart your terminal and server.`n"
}

Write-Host "`nALTERNATIVE: Run without image generation" -ForegroundColor Green
Write-Host "-----------------------------------------------------------"
Write-Host "Your app currently works fine - it just returns the original sketch"
Write-Host "instead of generating a new design. The Gemini prompts still work!`n"

Write-Host "Once you install the VC++ Redistributable, image generation will work.`n"
