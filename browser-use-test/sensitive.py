from dotenv import load_dotenv
import os
load_dotenv()

from browser_use.llm import ChatOpenAI, ChatGoogle
from browser_use import Agent, BrowserSession
import asyncio


# llm = ChatOpenAI(model='gpt-4.1-nano')
llm = ChatGoogle(model='gemini-2.0-flash')

x_mail = os.getenv('X_EMAIL')
x_pass = os.getenv('X_PASS')

# Domain-specific sensitive data
sensitive_data = {
    'https://*.google.com': {'x_email': x_mail, 'x_pass': x_pass},
    # 'chrome-extension://abcd1243': {'x_api_key': '...'},
    # 'http*://example.com': {'x_authcode': '123123'}
}

# Set browser session with allowed domains that match all domain patterns in sensitive_data
browser_session = BrowserSession(
    allowed_domains=[
        'https://*.google.com',
        # 'chrome-extension://abcd',
        # 'http://example.com',   # Explicitly include http:// if needed
        # 'https://example.com'   # By default, only https:// is matched
    ]
)

# Pass the sensitive data to the agent
agent = Agent(
    task="Log into Google, then check my account information",
    llm=llm,
    sensitive_data=sensitive_data,
    browser_session=browser_session,
    use_vision=False,
    save_conversation_path="logs/conversation"
)

async def main():
    await agent.run(max_steps=20)

if __name__ == '__main__':
    asyncio.run(main())