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


root_agent = RootAgent()


root_agent_var_name = 'root_agent'
if 'weather_agent_team' in globals():
    root_agent_var_name = 'weather_agent_team'

elif 'root_agent' not in globals():
    print("Root agent ('root agent' or 'weather_agent_team') not found. Cannot define run_team_conversation.")


if root_agent_var_name in globals() and globals()[root_agent_var_name]:

    async def run_team_conversation():
        print("\n --- Testing Agent Team Delegation --- ")
        session_service = InMemorySessionService()
        APP_NAME = "weather_tutorial_agent_team"
        USER_ID = "user_1_agent_team"
        SESSION_ID = "session_001_agent_team"
        session = await session_service.create_session(
            app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
        )
        print(f"Session Created: App='{APP_NAME}', User = '{USER_ID}', Session='{SESSION_ID}'")

        actual_root_agent = globals()[root_agent_var_name]
        runner_agent_team = Runner(
            agent=actual_root_agent,
            app_name=APP_NAME,
            session_service=session_service,
        )
        print(f"Runner created for agent '{actual_root_agent.name}'")

        await AgentAsync.call_agent_async(query = "Hello there!",
                               runner=runner_agent_team,
                               user_id=USER_ID,
                               session_id=SESSION_ID)
        await AgentAsync.call_agent_async(query = "What is the weather in New York?",
                               runner=runner_agent_team,
                               user_id=USER_ID,
                               session_id=SESSION_ID)
        await AgentAsync.call_agent_async(query = "Thanks, bye!",
                               runner=runner_agent_team,
                               user_id=USER_ID,
                               session_id=SESSION_ID)
        

    if __name__ == "__main__": # Ensures this runs only when script is executed directly
        print("Executing using 'asyncio.run()' (for standard Python scripts)...")
        try:
            # This creates an event loop, runs your async function, and closes the loop.
            asyncio.run(run_team_conversation())
        except Exception as e:
            print(f"An error occurred: {e}")

else:
    # This message prints if the root agent variable wasn't found earlier
    print("\n⚠️ Skipping agent team conversation execution as the root agent was not successfully defined in a previous step.")