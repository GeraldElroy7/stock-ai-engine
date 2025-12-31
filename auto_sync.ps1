# Auto-sync script for stock-ai-engine
# Run: powershell -File auto_sync.ps1

$repoPath = "C:\Users\Bittime\Documents\Script\stock_ai_engine"
$interval = 300  # 5 minutes in seconds

Write-Host "============================================" -ForegroundColor Cyan
Write-Host "Stock AI Engine - Auto-Sync to GitHub" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Repository: $repoPath" -ForegroundColor Yellow
Write-Host "Sync interval: $interval seconds (5 minutes)" -ForegroundColor Yellow
Write-Host "Token: Configured ✓" -ForegroundColor Green
Write-Host ""
Write-Host "Press CTRL+C to stop auto-sync" -ForegroundColor Magenta
Write-Host ""

$syncCount = 0

while ($true) {
    try {
        Set-Location $repoPath
        
        # Check if there are changes
        $status = git status --porcelain
        
        if ($status) {
            $syncCount++
            $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
            
            Write-Host "[$timestamp] ⚡ Changes detected (Sync #$syncCount)" -ForegroundColor Yellow
            
            # Stage all changes
            git add .
            
            # Commit
            $commitMsg = "Auto-sync: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
            git commit -m $commitMsg -q
            
            # Push
            git push -q 2>$null
            
            Write-Host "[$timestamp] ✅ Pushed to GitHub" -ForegroundColor Green
            Write-Host ""
        } else {
            $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
            Write-Host "[$timestamp] ⏸️  No changes detected, waiting..." -ForegroundColor Gray
        }
        
        # Wait for next check
        Start-Sleep -Seconds $interval
        
    } catch {
        $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
        Write-Host "[$timestamp] ❌ Error: $($_.Exception.Message)" -ForegroundColor Red
        Start-Sleep -Seconds 60  # Wait longer on error
    }
}
