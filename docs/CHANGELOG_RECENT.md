# Recent Changes (2025-12-31)

This file summarizes the latest changes applied on 2025-12-31.

- Added `results/` directory and save support for `/backtest` and `/analysis` endpoints (`save` flag).
- Added `data/fundamentals.py` to load provided fundamentals JSON files under `data/fund_data/`.
- Added `engine/ai_summary.py` which produces a templated AI-style summary combining technical & fundamental signals.
- Fixed JSON serialization issues for numpy scalars in backtest reports.
- Improved global exception handler to return JSON responses instead of raw tracebacks.
- Updated `main.py` to expose `/analysis` endpoint and to persist results when requested.

Saved results are written to `results/` as CSV (trades) and JSON (report/summary).
