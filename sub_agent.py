from google.adk.agents import Agent
from model import config, model_registry
from sub_agent_tools import sub_tools
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from weather_agent import AgentAsync
import asyncio

class SubAgent:
    
    def get_sub_agent():
        try:
            greeting_agent= Agent(
                model=model_registry.get_model("fast"),
                name="greeting_agent",
                instruction="You are the Greeting Agent. Your ONLY task is to provide a friendly greeting to the user. "
                                "Use the 'say_hello' tool to generate the greeting. "
                                "If the user provides their name, make sure to pass it to the tool. "
                                "Do not engage in any other conversation or tasks.",
                description="Handles simple greetings and hellos using the 'say_hello' tool.",

                tools=[sub_tools.say_hello]
            )

            print(f"Agent'{greeting_agent.name}' created using model '{greeting_agent.model}'.")
        except Exception as e:
            print(f" Could not create Greetings agent. Check API key ({greeting_agent.model}). Error: {e} ")


        try:
            farewell_agent = Agent(
                model = model_registry.get_model("fast"),
                name = "farewel_agent",
                instruction="You are the Farewell Agent. Your ONLY task is to provide a polite goodbye message. "
                            "Use the 'say_goodbye' tool when the user indicates they are leaving or ending the conversation "
                            "(e.g., using words like 'bye', 'goodbye', 'thanks bye', 'see you'). "
                            "Do not perform any other actions.",
                description="Handles simple farewells and goodbyes using the 'say_goodbye' tool.", 
                tools = [sub_tools.say_goodbye],
            )

            print(f"Agent '{farewell_agent.name}' created using model '{farewell_agent.model}'")
        except Exception as e:
            print(f" Could not create Farewell agent. Check API Key {{farewel_agent.model}}. Error: {e} ")


sub_agent = SubAgent()