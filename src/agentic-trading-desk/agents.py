from google.adk.tools import google_search
from google.adk.agents import Agent, ParallelAgent, SequentialAgent, LoopAgent
from google.adk.tools import google_search, ToolContext
from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService, Session
from google.genai.types import Content, Part

load_dotenv()
MODEL = "gemini-2.5-flash-lite"

# Specialist Agent 1
sentiment_scraper = Agent(
    name="sentiment_scraper_agent", model=MODEL,
    instruction="""
        Extract sentiments data for given stock {stock_symbol}. 
        Do: Focus on recent news and social media trends. 
        Don't: Include historical data older than 1 month.""",
    output_key="scraper_result",
    tools = [stock_data_tool]
)

# Specialist Agent 2
technical_analyst = Agent(
    name="technical_analyst_agent", model=MODEL,
    instruction="""
        Analyze ticker price and RSI levels to identify overbought (>70) or oversold (<30) conditions. 
        Signal 'Sell' if overbought and 'Buy' if oversold.
        """,
    output_key="technical_result",
    tools = [stock_data_tool]
)

# this is a synthesizer agent that combines information from data_miner & macro_observer
risk_gatekeeper = Agent(
    name="risk_gatekeeper_agent",
    model=MODEL,
    instruction="""Validate proposed trades against max_position_size and daily_loss_limit in the config.
    Do: Provide a hard "PASS" or "FAIL" based on the math. 
    Don't: Allow a trade to proceed if it exceeds a 2% account risk.""",
    tools = [risk_analysis_tool],
    output_key="narrative_result" # Set the correct output key for this workflow
)


trade_executioner = Agent(
    name="trade_executioner_agent",
    model=MODEL,
    instruction="""
    Act as the final decision-maker by requiring consensus between Sentiment and Technical agents.
    Technical analysis: {technical_result}
    Sentiment analysis: {scraper_result}
    Risk assessment: {narrative_result}
    Do: Execute only if both analysts agree AND Risk gives a 'PASS.'
    Don't: Trade during 'High Volatility' flags unless confidence is >90%.""",
    output_key="compliance_result" # Set the correct output key for this workflow
)



# The ParallelAgent runs all specialists at once
parallel_research_team = ParallelAgent(
    name="parallel_research_team",
    sub_agents=[sentiment_scraper, technical_analyst, risk_gatekeeper]
)


# The SequentialAgent runs the parallel search, then the synthesis
trading_team = SequentialAgent(
    name="trading_team",
    sub_agents=[parallel_research_team, trade_executioner],
    description="A workflow that finds multiple things in parallel and then summarizes the results."
)


root_agent = trading_team
print("Trading Agent team supercharged with a workflow!")

