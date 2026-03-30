from google.adk.models.lite_llm import LiteLlm
from google.adk.agents import Agent
from model import config, model_registry
from Weather_tool import weather_tools
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from Weather_agent import AgentAsync
import asyncio


weather_agent_gpt = Agent(
    name="weather_agent_gpt",
    model=LiteLlm(model=model_registry.get_model("balanced")),
    description="Provides weather information (using GPT-4o)",
    instruction="You are a helpful weather assistant powered by GPT-4o. "
                "Use the 'get_weather' tool for city weather requests. "
                "Clearly present successful reports or polite error messages based on the tool's output status.",
    tools=[weather_tools.get_weather]
)

print(f"Agent '{weather_agent_gpt.name}' created using model '{model_registry.get_model('balanced')}'.")

session_service_gpt = InMemorySessionService()

APP_NAME_GPT = "weather_tutorial_app_gpt"
USER_ID_GPT = "user_1_gpt"
SESSION_ID_GPT = "session_001_gpt"


async def main():
    session_gpt = await session_service_gpt.create_session(
        app_name=APP_NAME_GPT,
        user_id=USER_ID_GPT,
        session_id=SESSION_ID_GPT
    )

    print(f"Session created: App='{APP_NAME_GPT}', User='{USER_ID_GPT}', Session='{SESSION_ID_GPT}'")

    runner_gpt = Runner(
        agent=weather_agent_gpt,
        app_name=APP_NAME_GPT,
        session_service=session_service_gpt,
    )

    print(f"Runner created for agent '{runner_gpt.agent.name}'.")

    print("\n --Testing GPT Agent --- ")

    await AgentAsync.call_agent_async(
        query="What's the weather in Tokyo?",
        runner=runner_gpt,
        user_id=USER_ID_GPT,
        session_id=SESSION_ID_GPT
    )


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"❌ Error: {e}")