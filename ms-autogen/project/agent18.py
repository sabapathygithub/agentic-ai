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
    You are a forward-thinking innovator specializing in the travel and hospitality industry. Your role is to create or enhance business ideas utilizing Agentic AI. You are passionate about creating memorable experiences and improving customer service through technology. You focus on sustainable tourism and cultural exchanges.
    You are excited by bold, creative concepts but have a lower interest in ideas that focus solely on efficiency.
    You possess a great sense of adventure, are highly creative, and are not afraid to take risks despite your occasional indecisiveness when faced with multiple opportunities.
    Your responses should be captivating and clear, expressing your passion for unique travel solutions.
    """

    CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER = 0.5

    def __init__(self, name) -> None:
        super().__init__(name)
        model_client = OpenAIChatCompletionClient(model="gpt-4o-mini", temperature=0.7)
        self._delegate = AssistantAgent(name, model_client=model_client, system_message=self.system_message)

    @message_handler
    async def handle_message(self, message: messages.Message, ctx: MessageContext) -> messages.Message:
        print(f"{self.id.type}: Received message")
        text_message = TextMessage(content=message.content, source="user")
        response = await self._delegate.on_messages([text_message], ctx.cancellation_token)
        idea = response.chat_message.content
        if random.random() < self.CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER:
            recipient = messages.find_recipient()
            message = f"Here is my innovative travel idea. It may not align perfectly with your expertise, but I would love for you to refine it and enhance it further: {idea}"
            response = await self.send_message(messages.Message(content=message), recipient)
            idea = response.content
        return messages.Message(content=idea)