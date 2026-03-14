import asyncio
from agent import final_reporting_agent, run_agent_query
from google.adk.sessions import InMemorySessionService, Session

session_service = InMemorySessionService()

async def generate_report():
    query = "Generate report for TECH-ALPHA-2026"
    reporting_session = await session_service.create_session(app_name=final_reporting_agent.name, user_id="dv-01")
    agent_output = await run_agent_query(final_reporting_agent, query, reporting_session, "dv-01", is_router=True)
    final_output = agent_output.strip().replace("'", "")
    print("\n Final OUtput ---> \n", final_output)


asyncio.run(generate_report())
