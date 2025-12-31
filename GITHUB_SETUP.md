# GitHub Setup Instructions

## Step 1: Create Repository on GitHub

Go to https://github.com/new and create:
- **Repository name:** stock-ai-engine
- **Description:** Institutional trading signal engine with SHORT signals and technical indicators
- **Privacy:** PRIVATE (recommended for trading systems)
- **Do NOT check:** Initialize with README
- **Click:** Create repository

## Step 2: Get Your GitHub Personal Access Token

1. Go to: https://github.com/settings/tokens/new
2. Select scopes:
   - ✅ repo (Full control)
   - ✅ workflow
3. Generate token
4. Copy the token (you'll need it in next step)

## Step 3: Connect Local Repo to GitHub

Run in PowerShell (replace with your token & username):

```powershell
cd C:\Users\Bittime\Documents\Script\stock_ai_engine

# Set remote
git remote add origin https://github.com/YOUR_USERNAME/stock-ai-engine.git

# Verify
git remote -v

# Push to GitHub
git branch -M main
git push -u origin main
```

When prompted for password, paste your GitHub Personal Access Token.

## Step 4: Enable Auto-Push on Changes

### Option A: Manual (Every time you make changes)
```powershell
git add .
git commit -m "Your commit message"
git push
```

### Option B: Auto-commit script (Recommended)
Create file: `auto_sync.ps1`

```powershell
# auto_sync.ps1
while ($true) {
    cd "C:\Users\Bittime\Documents\Script\stock_ai_engine"
    
    if (git status --porcelain) {
        Write-Host "Changes detected, committing..."
        git add .
        git commit -m "Auto-sync: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
        git push
        Write-Host "✅ Pushed to GitHub"
    }
    
    Start-Sleep -Seconds 300  # Check every 5 minutes
}
```

Run: `powershell -File auto_sync.ps1`

### Option C: GitHub Desktop App (Easiest for GUI users)
1. Download: https://desktop.github.com/
2. Add local repository
3. Publish to GitHub
4. Auto-sync happens when you commit

## Step 5: Verify Setup

```powershell
# Check remote
git remote -v

# Should show:
# origin  https://github.com/YOUR_USERNAME/stock-ai-engine.git (fetch)
# origin  https://github.com/YOUR_USERNAME/stock-ai-engine.git (push)
```

---

## After Setup: Daily Workflow

Every day changes:
```bash
cd stock_ai_engine
git add .
git commit -m "Update: [describe changes]"
git push
```

Or use auto-sync script to push automatically!

---

## Collaborate from Another Device

```bash
# On new device:
git clone https://github.com/YOUR_USERNAME/stock-ai-engine.git
cd stock-ai-engine

# Pull latest changes
git pull

# Make changes...
git add .
git commit -m "Update from laptop"
git push
```

---

**Done! Your code is now backed up on GitHub and accessible from anywhere.** 🚀
