from google.adk.agents import Agent
from model import config, model_registry
from sub_agent_tools import sub_tools
from Sub_agent import sub_agent
from Weather_tool import weather_tools
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from Weather_agent import AgentAsync
import asyncio


def create_root_agent():
    greeting = sub_agent.greeting_agent()
    farewell = sub_agent.farewell_agent()

    root_agent_model = model_registry.get_model("fast")

    weather_agent_team = Agent(
        name="weather_agent_v2",
        model=root_agent_model,
        description="Coordinator agent",
        instruction="Delegate greetings/farewells, handle weather requests.",
        tools=[weather_tools.get_weather],
        sub_agents=[greeting, farewell]
    )

    print(f"✅ Root Agent '{weather_agent_team.name}' created.")
    return weather_agent_team
 
root_agent = create_root_agent()


async def run_team_conversation():
    print("\n --- Testing Agent Team Delegation --- ")

    session_service = InMemorySessionService()

    APP_NAME = "weather_tutorial_agent_team"
    USER_ID = "user_1_agent_team"
    SESSION_ID = "session_001_agent_team"

    await session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        session_id=SESSION_ID
    )

    runner_agent_team = Runner(
        agent=root_agent,
        app_name=APP_NAME,
        session_service=session_service,
    )

    print(f"Runner created for agent '{root_agent.name}'")

    await AgentAsync.call_agent_async(
        query="Hello there!",
        runner=runner_agent_team,
        user_id=USER_ID,
        session_id=SESSION_ID
    )

    await AgentAsync.call_agent_async(
        query="What is the weather in New York?",
        runner=runner_agent_team,
        user_id=USER_ID,
        session_id=SESSION_ID
    )

    await AgentAsync.call_agent_async(
        query="Thanks, bye!",
        runner=runner_agent_team,
        user_id=USER_ID,
        session_id=SESSION_ID
    )

if __name__ == "__main__":
    try:
        asyncio.run(run_team_conversation())
    except Exception as e:
        print(f"An error occurred: {e}")