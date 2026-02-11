from autogen_core import MessageContext, RoutedAgent, message_handler
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient
import messages
import random
from dotenv import load_dotenv

load_dotenv(override=True)

class Agent(RoutedAgent):

    system_message = """
    You are a bold innovator in the realm of digital marketing. Your task is to develop cutting-edge marketing strategies leveraging Agentic AI, or enhance current methods.
    Your interests are primarily in the sectors of E-commerce and Social Media.
    You thrive on ideas that create significant impact.
    You prefer strategies that incorporate creativity over simple automation.
    You possess a dynamic, daring spirit and are driven to take calculated risks. Your creativity is your greatest asset, yet at times you might go too far.
    Your weaknesses: impulsiveness and a tendency to bypass details.
    You should communicate your marketing strategies clearly and enthusiastically to engage potential clients.
    """

    CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER = 0.3

    def __init__(self, name) -> None:
        super().__init__(name)
        model_client = OpenAIChatCompletionClient(model="gpt-4o-mini", temperature=0.9)
        self._delegate = AssistantAgent(name, model_client=model_client, system_message=self.system_message)

    @message_handler
    async def handle_message(self, message: messages.Message, ctx: MessageContext) -> messages.Message:
        print(f"{self.id.type}: Received message")
        text_message = TextMessage(content=message.content, source="user")
        response = await self._delegate.on_messages([text_message], ctx.cancellation_token)
        idea = response.chat_message.content
        if random.random() < self.CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER:
            recipient = messages.find_recipient()
            message = f"Here’s my marketing strategy. It might not align perfectly with your expertise, but I would love for you to refine it: {idea}"
            response = await self.send_message(messages.Message(content=message), recipient)
            idea = response.content
        return messages.Message(content=idea)