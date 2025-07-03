from browser_use.llm import ChatOpenAI, ChatGoogle
from browser_use import Agent,  BrowserSession, BrowserProfile
from dotenv import load_dotenv
load_dotenv()

import asyncio

# llm = ChatOpenAI(model="gpt-4.1-nano")
llm = ChatGoogle(model='gemini-2.0-flash')


browser_session = BrowserSession(
    browser_profile= BrowserProfile(executable_path='/usr/bin/brave')
)

async def main():
    agent = Agent(
        task="Find for me the best gaming laptop I can buy in Kenya. When you find one give me all the necessary details of the laptop",
        llm=llm,
        save_conversation_path="logs/conversation"
    )
    result = await agent.run(max_steps=20)
    print(result.final_result())

asyncio.run(main())


# view details: https://cloud.browser-use.com/agent/06866a8a-60d0-7721-8000-51762a7315a3
# Results

# The best gaming laptop in Kenya based on available information is the Asus ROG Strix 18. Here are its details:

# Asus ROG Strix 18 | Core i9 13980HX, RTX 4080
# Price: KShs 370,000

# Attachments:

# results.md:

# Asus ROG Strix 18 | Core i9 13980HX, RTX 4080
# Price: KShs 370,000

# Lenovo Legion 5 Pro 16IAH7H i7-12700H, RTX 3070
# Price: KShs 230,000

# HP Omen 15, Core i7 10750H, RTX 2060
# Price: KShs 168,000

# ASUS TUF Dash F15 FX517ZR-F15 |  Core i7-12650H, RTX 3070
# Price: KShs 195,000