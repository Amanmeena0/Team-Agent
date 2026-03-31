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
from BothGuardrailAgent import runner_root_tool_guardrail


async def run_tool_guardrail_test():
    print("\n--- Testing Tool Argument Guardrail ('Paris' blocked) ---")
     # ✅ STEP 1: CREATE SESSION (MANDATORY)
    await session_service_stateful.create_session(
        app_name=APP_NAME,
        user_id=USER_ID_STATEFUL,
        session_id=SESSION_ID_STATEFUL
    )
    
    interaction_func = lambda query: AgentAsync.call_agent_async(
        query,
        runner_root_tool_guardrail,
        USER_ID_STATEFUL,
        SESSION_ID_STATEFUL
    )

    print("--- Turn 1: Requesting weather in New York (expect allowed) ---")
    await interaction_func("What's the weather in New York?")

    print("\n--- Turn 2: Requesting weather in Paris (expect blocked) ---")
    await interaction_func("How about Paris?")

    print("\n--- Turn 3: Requesting weather in London (expect allowed) ---")
    await interaction_func("Tell me the weather in London.")

    # ✅ Move session inspection INSIDE async function
    print("\n--- Inspecting Final Session State ---")

    final_session = await session_service_stateful.get_session(
        app_name=APP_NAME,
        user_id=USER_ID_STATEFUL,
        session_id=SESSION_ID_STATEFUL
    )

    if final_session:
        print(f"Tool Guardrail Triggered: {final_session.state.get('guardrail_tool_block_triggered', False)}")
        print(f"Last Weather Report: {final_session.state.get('last_weather_report', 'Not Set')}")
        print(f"Temperature Unit: {final_session.state.get('user_preference_temperature_unit', 'Not Set')}")
    else:
        print("❌ Error: Could not retrieve final session state.")


if __name__ == "__main__":
    print("Executing with asyncio.run()...")
    try:
        asyncio.run(run_tool_guardrail_test())
    except Exception as e:
        print(f"❌ Runtime Error: {e}")