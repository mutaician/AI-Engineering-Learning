from browser_use import Agent, BrowserSession
from browser_use.llm import ChatOpenAI
import asyncio

# If no executable_path provided, uses Playwright/Patchright's built-in Chromium
browser_session = BrowserSession(
    # Path to a specific Chromium-based executable (optional)
    # executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',  # macOS
    # For Windows: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
    # For Linux: '/usr/bin/brave'
    executable_path='/usr/bin/brave', # type: ignore

    # Use a specific data directory on disk (optional, set to None for incognito)
    user_data_dir='~/.config/browseruse/profiles/default',   # this is the default # type: ignore
    # ... any other BrowserProfile or playwright launch_persistnet_context config...
    # headless=False,
)

llm = ChatOpenAI(model="gpt-4.1-nano")

async def main():
    agent = Agent(
        task="open google docs",
        llm=llm,
        browser_session=browser_session,
        save_conversation_path="logs/conversation"
    )

    result = await agent.run(max_steps=20)
    print(result)

asyncio.run(main())