import asyncio
from agent import final_reporting_agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService, Session
from google.genai import types

APP_NAME = "reporting-app"
USER_ID = "12345"
SESSION_ID = "123344"

# Session and Runner
async def setup_session_and_runner():
    session_service = InMemorySessionService()
    session = await session_service.create_session(app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID)
    runner = Runner(agent=final_reporting_agent, app_name=APP_NAME, session_service=session_service)
    return session, runner


# Agent Interaction
async def call_agent_async(query):
    content = types.Content(role='user', parts=[types.Part(text=query)])
    session, runner = await setup_session_and_runner()
    events = runner.run_async(user_id=USER_ID, session_id=SESSION_ID, new_message=content)

    async for event in events:
        if event.is_final_response():
            final_response = event.content.parts[0].text
            print("Agent Response: ", final_response)

asyncio.run(call_agent_async("generate report for TECH-ALPHA-2026"))
