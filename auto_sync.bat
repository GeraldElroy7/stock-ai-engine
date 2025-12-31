@echo off
REM Auto-sync script for stock-ai-engine
REM This script automatically pushes changes to GitHub every 5 minutes

setlocal enabledelayedexpansion

set "REPO_PATH=C:\Users\Bittime\Documents\Script\stock_ai_engine"
set "INTERVAL=300"

echo ============================================
echo Stock AI Engine - Auto-Sync to GitHub
echo ============================================
echo.
echo Repo: %REPO_PATH%
echo Interval: %INTERVAL% seconds (5 minutes)
echo.
echo Press CTRL+C to stop auto-sync
echo.

:loop
cd /d "%REPO_PATH%"

REM Check if there are any changes
git status --porcelain >nul 2>&1
if not errorlevel 1 (
    for /f %%i in ('git status --porcelain') do (
        set "has_changes=true"
    )
)

if defined has_changes (
    echo [%date% %time%] Changes detected, committing...
    git add .
    git commit -m "Auto-sync: %date% %time%"
    git push
    echo [%date% %time%] ✅ Pushed to GitHub
    set "has_changes="
) else (
    echo [%date% %time%] No changes detected, waiting...
)

timeout /t %INTERVAL% /nobreak
goto loop
