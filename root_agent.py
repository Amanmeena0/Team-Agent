from google.adk.agents import Agent
from model import config, model_registry
from sub_agent_tools import sub_tools
from Sub_agent import sub_agent
from Weather_tool import weather_tools
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from Weather_agent import AgentAsync
import asyncio


class RootAgent:
    def root_agent():
        
        if sub_agent.greeting_agent and sub_agent.farewell_agent and 'get_weather' in globals():
            root_agent_model = model_registry.get_model("fast")

            weather_agent_team = Agent(
                name = "weather_agent_v2",
                model=root_agent_model,
                description="The main coordinator agent. Handles weather requests and delegates greetings/farewells to specialists.",
                instruction="You are the main Weather Agent coordinating a team. Your primary responsibility is to provide weather information. "
                    "Use the 'get_weather' tool ONLY for specific weather requests (e.g., 'weather in London'). "
                    "You have specialized sub-agents: "
                    "1. 'greeting_agent': Handles simple greetings like 'Hi', 'Hello'. Delegate to it for these. "
                    "2. 'farewell_agent': Handles simple farewells like 'Bye', 'See you'. Delegate to it for these. "
                    "Analyze the user's query. If it's a greeting, delegate to 'greeting_agent'. If it's a farewell, delegate to 'farewell_agent'. "
                    "If it's a weather request, handle it yourself using 'get_weather'. "
                    "For anything else, respond appropriately or state you cannot handle it.",
                tools=[weather_tools.get_weather],
                sub_agents= [sub_agent.greeting_agent , sub_agent.farewell_agent]
            )
            print(f"✅ Root Agent '{weather_agent_team.name}' created using model '{root_agent_model}' with sub-agents: {[sa.name for sa in weather_agent_team.sub_agents]}")

        else:
            print("❌ Cannot create root agent because one or more sub-agents failed to initialize or 'get_weather' tool is missing.")
            if not sub_agent.greeting_agent: print(" - Greeting Agent is missing.")
            if not sub_agent.farewell_agent: print(" - Farewell Agent is missing.")
            if 'get_weather' not in globals(): print(" - get_weather function is missing.")


            