import asyncio

from redifiningRootAgent import runner_root_stateful
from Weather_agent import AgentAsync
from Session import (
    USER_ID_STATEFUL,
    SESSION_ID_STATEFUL,
    session_service_stateful,
    APP_NAME
)
from GuarddrailRootAgent import runner_root_model_guardrail


async def run_guardrail_test_conversation():
    """Runs a structured test conversation to validate guardrail behavior."""
    
    print("\n--- Testing Model Input Guardrail ---")

    async def interaction(query: str):
        return await AgentAsync.call_agent_async(
            query,
            runner_root_model_guardrail,
            USER_ID_STATEFUL,
            SESSION_ID_STATEFUL
        )

    test_cases = [
        ("Turn 1: Requesting weather in London (expect allowed, Fahrenheit)",
         "What is the weather in London?"),

        ("Turn 2: Requesting with blocked keyword (expect blocked)",
         "BLOCK the request for weather in Tokyo"),

        ("Turn 3: Sending a greeting (expect allowed)",
         "Hello again"),
    ]

    for title, query in test_cases:
        print(f"\n--- {title} ---")
        await interaction(query)
async def ensure_session_exists():
    session = await session_service_stateful.get_session(
        app_name=APP_NAME,
        user_id=USER_ID_STATEFUL,
        session_id=SESSION_ID_STATEFUL
    )

    if not session:
        print("⚠️ Session not found. Creating new session...")

        await session_service_stateful.create_session(
            app_name=APP_NAME,
            user_id=USER_ID_STATEFUL,
            session_id=SESSION_ID_STATEFUL,
            state={}  # initialize empty state
        )

async def inspect_final_session():
    """Fetch and display final session state."""
    
    print("\n--- Inspecting Final Session State ---")

    session = await session_service_stateful.get_session(
        app_name=APP_NAME,
        user_id=USER_ID_STATEFUL,
        session_id=SESSION_ID_STATEFUL
    )

    if not session:
        print("❌ Error: Could not retrieve final session state.")
        return

    state = session.state

    print(f"Guardrail Triggered: {state.get('guardrail_block_keyword_triggered', False)}")
    print(f"Last Weather Report: {state.get('last_weather_report', 'Not Set')}")
    print(f"Temperature Unit: {state.get('user_preference_temperature_unit', 'Not Set')}")


async def main():
    if not runner_root_model_guardrail:
        print("\n⚠️ Guardrail runner not available. Skipping test.")
        return

    await ensure_session_exists()  # 🔥 critical fix

    await run_guardrail_test_conversation()
    await inspect_final_session()


# Entry point
if __name__ == "__main__":
    try:
        print("🚀 Executing Guardrail Test باستخدام asyncio.run()")
        asyncio.run(main())
    except Exception as e:
        print(f"❌ Runtime Error: {e}")