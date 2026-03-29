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