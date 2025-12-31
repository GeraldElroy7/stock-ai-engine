import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

try:
    import engine.ai_agent as aa
    import engine.ai_summary as asu
    import data.fetchers.yahoo_fundamentals as yf_f
    import data.fetcher as df
    import indicators.technical as it
    print('IMPORT_OK')
except Exception as e:
    import traceback
    traceback.print_exc()
    print('IMPORT_FAIL', e)
