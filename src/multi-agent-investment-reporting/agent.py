from google.adk.tools import google_search
from google.adk.agents import Agent, ParallelAgent, SequentialAgent, LoopAgent
from google.adk.tools import google_search, ToolContext
from dotenv import load_dotenv
from tools import fetch_portfolio_data, get_compliance_config
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService, Session
from google.genai.types import Content, Part

load_dotenv()

# Specialist Agent 1
data_miner = Agent(
    name="data_miner_agent", model="gemini-2.5-flash",
    instruction="Extract and calculate performance deltas from the JSON for a specific ID. Do: Use exact numbers; calculate Alpha ($Return - Benchmark$). Don't: Add any commentary or opinions.",
    output_key="miner_result",
    tools = [fetch_portfolio_data]
)

# Specialist Agent 2
macro_observer = Agent(
    name="macro_observer_agent", model="gemini-2.5-flash",
    instruction="Correlate the attribution reason with the provided market context. Do: Create a logical link between 'Market Context' and 'Sector Impact'. Don't: Invent external news not found in the JSON.",
    output_key="observer_result",
    tools = [fetch_portfolio_data]
)

# this is a synthesizer agent that combines information from data_miner & macro_observer
narrative_architect = Agent(
    name="narrative_architect_agent",
    model="gemini-2.5-flash",
    instruction="""Combine the following research results into a clear and professional client commentary. 
    - Performance stats : {miner_result}
    - Market context : {observer_result}
    Do: Use formal language; keep it under 100 words per portfolio. 
    Don't: Use jargon that a retail client wouldn't understand.""",
    output_key="narrative_result" # Set the correct output key for this workflow
)


compliance_guardian = Agent(
    name="compliance_guardian_agent",
    model="gemini-2.5-flash",
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

