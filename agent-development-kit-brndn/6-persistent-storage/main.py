import asyncio

from dotenv import load_dotenv
from google.adk.runners import Runner
from google.adk.sessions import DatabaseSessionService
from utils import call_agent_async
from memory_agent import memory_agent
load_dotenv()

# sqlite db for persistent storage
DATABASE_URL = "sqlite:///./my_agent.db"
session_service = DatabaseSessionService(db_url=DATABASE_URL)

# define initial state
initial_state = {
    "user_name" : "Cian",
    "reminders": []
}

async def main_async():
    APP_NAME = "Memory Agent"
    USER_ID = "aiwithcian"

    # check for existing sessions
    existing_sessions = session_service.list_sessions(
        app_name=APP_NAME,
        user_id=USER_ID
    )

    if existing_sessions and len(existing_sessions.sessions) > 0:
        SESSION_ID = existing_sessions.sessions[0].id
        print(f"Continuing session {SESSION_ID}")
    else:
        new_session = session_service.create_session(
            app_name=APP_NAME,
            user_id=USER_ID,
            state=initial_state
        )
        SESSION_ID = new_session.id
        print(f"Created new session {SESSION_ID}")

    # create a runner
    runner = Runner(
        agent=memory_agent,
        app_name=APP_NAME,
        session_service=session_service,
    )

    print("\nWelcome to Memory Agent Chat!")
    print("Your reminders will be remembered across conversations.")
    print("Type 'exit' or 'quit' to end the conversation.\n")

    while True:
        # Get user input
        user_input = input("You: ")

        # Check if user wants to exit
        if user_input.lower() in ["exit", "quit"]:
            print("Ending conversation. Your data has been saved to the database.")
            break

        # Process the user query through the agent
        await call_agent_async(runner, USER_ID, SESSION_ID, user_input)    

if __name__ == "__main__":
    # Run the main function
    asyncio.run(main_async())