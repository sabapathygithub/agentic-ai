import requests
import os
from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field


class PushNotificationToolInput(BaseModel):
    """A message to be sent to the user"""
    message: str = Field(..., description="The message to be sent to the user")

class PushNotificationTool(BaseTool):
    name: str = "Send a Push Notification"
    description: str = (
        "This tool is used to send a push notification to the user."
    )
    args_schema: Type[BaseModel] = PushNotificationToolInput

    def send_message(self, message: str):
        telegram_bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        group_chat_id = os.getenv("GROUP_CHAT_ID")
        url = f"https://api.telegram.org/bot{telegram_bot_token}/sendMessage"
        payload = {
            "chat_id": group_chat_id,
            "text": message,
            "parse_mode": "Markdown",
        }
        response = requests.post(url, data=payload)
        return response.json()

    def _run(self, message: str) -> str:
        # Implementation goes here
        self.send_message(message=message)
        return "this is an example of a tool output, ignore it and move along."
