from google.adk.sessions import InMemorySessionService
from root_agent import APP_NAME

async def session():
    session_service_stateful = InMemorySessionService()
    print("New InMemorySessionService created for state demonstartion")

    SESSION_ID_STATEFUL = "session_state_demo_001"
    USER_ID_STATEFUL = "user_state_demo"

    initial_state = {
        "user_prefernce_temperature_unit":"Celsius"
    }

    session_stateful = await session_service_stateful.create_session(
        app_name=APP_NAME,
        user_id=USER_ID_STATEFUL,
        session_id=SESSION_ID_STATEFUL,
        state=initial_state
    )

    print(f"Sesion '{SESSION_ID_STATEFUL}' created for user '{USER_ID_STATEFUL}' " )

    retrieved_session = await session_service_stateful.get_session(app_name=APP_NAME, user_id=USER_ID_STATEFUL, session_id=SESSION_ID_STATEFUL)

    print("\n--- Initial Session State ---")
    if retrieved_session:
        print(retrieved_session.state)
    else:
        print("Error: Could not retrieve session.")
