import json

def fetch_portfolio_data(portfolio_id: str) -> dict:
    """Retrieves metrics and context for a specific portfolio from local JSON."""
    with open('data.json', 'r') as f:
        db = json.load(f)
    for p in db['portfolios']:
        if p['id'] == portfolio_id:
            return p
    return {}

def get_compliance_config() -> dict:
    """Retrieves mandatory legal disclaimers and banned words."""
    with open('data.json', 'r') as f:
        return json.load(f)['compliance_rules']