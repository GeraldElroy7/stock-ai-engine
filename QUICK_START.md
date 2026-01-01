# Quick Start Guide

## ✓ Setup Complete - Your Project is Ready!

### Verify Installation (Copy & Paste):
```bash
cd ~/stock-ai-engine
python3 --version
python3 -c "import pandas, numpy, yfinance, fastapi; print('All dependencies OK!')"
```

### Start the API Server:
```bash
cd ~/stock-ai-engine
python3 -m uvicorn main:app --reload
```
→ Visit: http://localhost:8000/docs

### Open in VS Code:
```bash
code ~/stock-ai-engine
```

### Run Tests:
```bash
cd ~/stock-ai-engine
python3 -m pytest tests/ -v
```

### Useful Commands:
- Install a new package: `python3 -m pip install <package-name>`
- Freeze dependencies: `python3 -m pip freeze > requirements.txt`
- Check Python version: `python3 --version`
- View installed packages: `python3 -m pip list`

### Troubleshooting:
- If `python3 --version` shows 3.9: Run `exec zsh` to reload shell config
- Missing dependencies: Run `python3 -m pip install -r requirements.txt`

---

**Project:** stock-ai-engine  
**Status:** ✓ Ready to use  
**Python:** 3.11.14
