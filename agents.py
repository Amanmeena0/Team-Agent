import os
import asyncio
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types

import warnings

warnings.filterwarnings("ignore")

import logging
logging.basicConfig(level=logging.ERROR)

from model import config,model_registry
from tools import weather_tools


weather_agent = Agent(
    name = "weather_agent_v1",
    model=model_registry.get_model("fast"),
    description="Provides weather information for specific cities.",
    instruction="You are a helpful weather assistant. "
                "When the user asks for the weather in a specific city, "
                "use the 'get_weather' tool to find the information. "
                "If the tool returns an error, inform the user politely. "
                "If the tool is successful, present the weather report clearly.",
    tools=[weather_tools.get_weather]
)

print(f"Agent '{weather_agent.name}' created using model '{model_registry.get_model('fast')}'")


session_service = InMemorySessionService()

APP_NAME = "weather_tutorial_app"
USER_ID = "user_1"
SESSION_ID = "session_01"

# session = await session_service.create_session(
#     app_name=APP_NAME,
#     user_id=USER_ID,
#     session_id=SESSION_ID,
# )
# print(f"Session created: App='{APP_NAME}', User='{USER_ID}', Session='{SESSION_ID}'")


async def init_session(app_name:str,user_id:str,session_id:str) -> InMemorySessionService:
    session = await session_service.create_session(
        app_name=app_name,
        user_id=user_id,
        session_id=session_id
    )
    print(f"Session created: App='{app_name}', User='{user_id}', Session='{session_id}'")
    return session

session = asyncio.run(init_session(APP_NAME,USER_ID,SESSION_ID))


runner = Runner (
    agent=weather_agent,
    app_name=APP_NAME,
    session_service=session_service
)

print(f"Runner created for agent '{runner.agent.name}'.")