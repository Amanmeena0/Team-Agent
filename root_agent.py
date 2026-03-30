from google.adk.agents import Agent
from model import config, model_registry
from sub_agent_tools import sub_tools
from sub_agent import sub_agent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from weather_agent import AgentAsync
import asyncio


class RootAgent:
    def root_agent():
        
        if sub_agent. and farewell_agent and 'get_weather' in globals():