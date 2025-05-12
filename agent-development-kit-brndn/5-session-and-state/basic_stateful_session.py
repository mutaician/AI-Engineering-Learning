import uuid
from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from question_answering_agent import question_answering_agent

load_dotenv()

# new session service to store state
session_service_stateful = InMemorySessionService()

initial_state = {
    "user_name": "Cyprian Kiplangat",
    "user_preferences": """
        I like to play with Generative AI
        I am an AI Engineer.
        Loves to talk about Technology, Philosophy, Time Travel, Future.
        My favourite TV Show is Black Mirror.
        I go by the username mutaician in most of my social media."""
}

# Create a NEW Session
APP_NAME = "Cian Bot"
USER_ID = "mutaician"
SESSION_ID = str(uuid.uuid4())

stateful_session = session_service_stateful.create_session(
    app_name=APP_NAME,
    user_id=USER_ID,
    session_id=SESSION_ID,
    state=initial_state
)

print("CREATED NEW SESSION")
print(f"\tSession ID: {SESSION_ID}")

runner = Runner(
    agent=question_answering_agent,
    app_name=APP_NAME,
    session_service=session_service_stateful
)

new_message = types.Content(
    role="user",
    parts=[types.Part(text="what's Cyprian's github account")]
)

for event in runner.run(
    user_id=USER_ID,
    session_id=SESSION_ID,
    new_message=new_message
) : 
    if event.is_final_response():
        if event.content and event.content.parts:
            print(f"Final Response: {event.content.parts[0].text}")

# print("==== Session Event Exploration ====")
# session = session_service_stateful.get_session(
#     app_name=APP_NAME, user_id=USER_ID, session_id=SESSION_ID
# )

# # Log final Session state
# print("=== Final Session State ===")
# for key, value in session.state.items():
#     print(f"{key}: {value}")