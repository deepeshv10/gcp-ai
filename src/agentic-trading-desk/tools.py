import json

def stock_data_tool() -> dict:
    """Retrieves technical analysis and market sentiments and context from local JSON."""
    try:
        with open('data.json', 'r') as f:
            return json.load(f)["live_market"]
    except (FileNotFoundError, KeyError):
        return {}

def risk_analysis_tool() -> dict:
    """Retrieves risk parameters."""
    try:
        with open('data.json', 'r') as f:
            return json.load(f)['risk_params']
    except (FileNotFoundError, KeyError):
        return {}