from google.adk.tools import google_search
from google.adk.agents import Agent, ParallelAgent, SequentialAgent, LoopAgent
from google.adk.tools import google_search, ToolContext
from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService, Session
from google.genai.types import Content, Part

load_dotenv()

# Specialist Agent 1
sentiment_scraper = Agent(
    name="sentiment_scraper_agent", model="gemini-2.5-flash-lite",
    instruction="""
        Extract sentiments data for given stock {stock_symbol}. 
        Do: Focus on recent news and social media trends. 
        Don't: Include historical data older than 1 month.""",
    output_key="scraper_result",
    tools = [sentiment_data_tool]
)

# Specialist Agent 2
technical_analyst = Agent(
    name="technical_analyst_agent", model="gemini-2.5-flash-lite",
    instruction="""
        Analyze ticker price and RSI levels to identify overbought (>70) or oversold (<30) conditions. 
        Signal 'Sell' if overbought and 'Buy' if oversold.
        """,
    output_key="technical_result",
    tools = [technical_analysis_tool]
)

# this is a synthesizer agent that combines information from data_miner & macro_observer
risk_gatekeeper = Agent(
    name="risk_gatekeeper_agent",
    model="gemini-2.5-flash-lite",
    instruction="""Combine the following research results into a clear and professional client commentary. 
    - Performance stats : {miner_result}
    - Market context : {observer_result}
    Do: Use formal language; keep it under 100 words per portfolio. 
    Don't: Use jargon that a retail client wouldn't understand.""",
    output_key="narrative_result" # Set the correct output key for this workflow
)


compliance_guardian = Agent(
    name="compliance_guardian_agent",
    model="gemini-2.5-flash-lite",
    tools=[get_compliance_config],
    instruction="Audit the final text for banned words and ensure the mandatory disclaimer is appended. Do: Strip banned words; verify the exact disclaimer string exists. Don't: Modify the financial data or macro reasoning.",
    output_key="compliance_result" # Set the correct output key for this workflow
)



# The ParallelAgent runs all specialists at once
parallel_research_agent = ParallelAgent(
    name="parallel_research_agent",
    sub_agents=[data_miner, macro_observer]
)


# The SequentialAgent runs the parallel search, then the synthesis
final_reporting_agent = SequentialAgent(
    name="final_reporting_agent",
    sub_agents=[parallel_research_agent, narrative_architect, compliance_guardian],
    description="A workflow that finds multiple things in parallel and then summarizes the results."
)

root_agent = final_reporting_agent
print("Reporting Agent team supercharged with a workflow!")

