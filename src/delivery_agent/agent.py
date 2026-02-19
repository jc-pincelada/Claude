"""Core agent module — wraps the Anthropic API with conversation management."""

from anthropic import Anthropic

from delivery_agent.prompts import SYSTEM_PROMPT

DEFAULT_MODEL = "claude-sonnet-4-5-20250929"
MAX_TOKENS = 8192


class DeliveryAgent:
    """A conversational agent specialized in SDLC and service delivery."""

    def __init__(self, model: str = DEFAULT_MODEL):
        self.client = Anthropic()  # reads ANTHROPIC_API_KEY from env
        self.model = model
        self.conversation: list[dict] = []

    def chat(self, user_message: str) -> str:
        """Send a message and return the assistant's response."""
        self.conversation.append({"role": "user", "content": user_message})

        response = self.client.messages.create(
            model=self.model,
            max_tokens=MAX_TOKENS,
            system=SYSTEM_PROMPT,
            messages=self.conversation,
        )

        assistant_text = response.content[0].text
        self.conversation.append({"role": "assistant", "content": assistant_text})
        return assistant_text

    def reset(self):
        """Clear conversation history."""
        self.conversation.clear()
