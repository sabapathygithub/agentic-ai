import sys
from playwright.async_api import async_playwright
from langchain_community.agent_toolkits import PlayWrightBrowserToolkit
from dotenv import load_dotenv
import os
from langchain_core.tools import Tool
from langchain_community.agent_toolkits import FileManagementToolkit
from langchain_community.tools.wikipedia.tool import WikipediaQueryRun
from langchain_experimental.tools import PythonREPLTool
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_community.utilities.wikipedia import WikipediaAPIWrapper
import requests

load_dotenv(override=True)

serper = GoogleSerperAPIWrapper()

# Defining PlayWright tools which similiar like selenium web automation tool.
async def playwright_tools():
    playwright = await async_playwright().start()
    browser =await playwright.chromium.launch(headless=False)
    toolkit = PlayWrightBrowserToolkit.from_browser(async_browser=browser)
    return toolkit.get_tools(), browser, playwright

def send_message(message: str):
    telegram_bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
    group_chat_id = os.getenv('GROUP_CHAT_ID')
    url = f"https://api.telegram.org/bot{telegram_bot_token}/sendMessage"
    payload = {
        "chat_id": group_chat_id,
        "text": message,
        "parse_mode": "Markdown",
    }
    response = requests.post(url, data=payload)
    return response.json()

def push(text: str) -> str:
    """Send a push notification to the user"""
    result = send_message(text)
    return 'success'

def get_file_tools():
    toolkit = FileManagementToolkit(root_dir="sandbox")
    return toolkit.get_tools()

async def other_tools():
    push_tool = Tool(name="send_push_notification", func=push, description="Use this tool when you want to send a push notificaction")
    file_tools = get_file_tools()
    search_tool = Tool(name="search", func=serper.run, description="Use this tool when you want to get the result of an online web search")
    
    wikipedia = WikipediaAPIWrapper()
    wiki_tool = WikipediaQueryRun(api_wrapper=wikipedia)

    python_repl = PythonREPLTool()
    return file_tools + [push_tool, search_tool, wiki_tool, python_repl]
