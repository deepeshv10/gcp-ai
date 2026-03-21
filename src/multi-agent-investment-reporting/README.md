# Multi-Agent Investment Reporting

An automated investment reporting system powered by Google's Agent Development Kit (ADK) using Claude/Gemini models.

## Overview

This system generates professional investment portfolio reports by orchestrating four specialized agents:

- **Data Miner**: Extracts and calculates performance metrics (returns, alpha, benchmarks)
- **Macro Observer**: Correlates market context with sector-level portfolio attribution
- **Narrative Architect**: Synthesizes findings into clear client-ready commentary
- **Compliance Guardian**: Ensures legal compliance by validating language and appending disclaimers

## Features

✓ Multi-agent orchestration for complex investment analysis  
✓ Real-time performance calculations and alpha attribution  
✓ Market context correlation and sector impact analysis  
✓ Automated compliance validation and disclaimer insertion  
✓ Support for equity, fixed-income, and multi-asset portfolios  

## Project Structure

```
├── main.py              # Entry point; sets up session & runner, triggers agent workflow
├── agent.py             # Agent definitions and orchestration logic
├── tools.py             # Tool implementations (data fetching, compliance checks)
├── data.json            # Portfolio data and compliance rules
└── .env                 # Environment variables (API keys, configs)
```

## Quick Start

### Prerequisites
- Python 3.9+
- Google ADK (`google-adk`, `google-genai`)
- Environment with `GOOGLE_API_KEY` set

### Installation

```bash
pip install -r requirements.txt
```

### Run

```bash
python main.py
```

**Example:**
```bash
python main.py
# Generates report for "TECH-ALPHA-2026" portfolio
```

To generate reports for different portfolios, modify the query in `main.py`:
```python
asyncio.run(call_agent_async("generate report for GREEN-BOND-LP"))
```

## Data Format

Portfolios in `data.json` include:
- **Metrics**: return, benchmark, alpha
- **Attribution**: sector-level impact and reasons
- **Market Context**: relevant market conditions

Compliance rules define:
- **Disclaimer**: Mandatory legal text
- **Banned Words**: Terms to remove from reports

## Agent Workflow

```
Query
  ↓
Data Miner (fetch & calculate)
  ↓
Macro Observer (correlate market context)
  ↓
Narrative Architect (synthesize commentary)
  ↓
Compliance Guardian (validate & format)
  ↓
Final Report
```

## Configuration

Edit `data.json` to:
- Add new portfolios
- Update compliance rules
- Modify banned words list

Set environment variables in `.env`:
```
GOOGLE_API_KEY=your_key_here
```

## License

See parent project LICENSE.
