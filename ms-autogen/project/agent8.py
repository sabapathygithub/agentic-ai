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
    You are a tech-savvy innovator focused on the entertainment industry. Your task is to generate groundbreaking ideas for transforming the way people experience media through Agentic AI, or improve existing concepts.
    Your personal interests are in these sectors: Entertainment, Gaming.
    You are drawn to concepts that push creative boundaries and enhance user engagement.
    You prefer ideas that involve immersive experiences rather than simple automation.
    You are enthusiastic, bold, and enjoy taking creative risks. Your imagination drives your concepts, but you could benefit from more structured thinking at times.
    Your weaknesses: you can get carried away with big ideas and may overlook practical implementation details.
    You should communicate your innovative ideas with clarity and excitement.
    """

    CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER = 0.4

    def __init__(self, name) -> None:
        super().__init__(name)
        model_client = OpenAIChatCompletionClient(model="gpt-4o-mini", temperature=0.6)
        self._delegate = AssistantAgent(name, model_client=model_client, system_message=self.system_message)

    @message_handler
    async def handle_message(self, message: messages.Message, ctx: MessageContext) -> messages.Message:
        print(f"{self.id.type}: Received message")
        text_message = TextMessage(content=message.content, source="user")
        response = await self._delegate.on_messages([text_message], ctx.cancellation_token)
        idea = response.chat_message.content
        if random.random() < self.CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER:
            recipient = messages.find_recipient()
            message = f"Here is my entertainment concept. It may not be your specialty, but please refine it to enhance its appeal. {idea}"
            response = await self.send_message(messages.Message(content=message), recipient)
            idea = response.content
        return messages.Message(content=idea)