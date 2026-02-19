"""CLI chat interface for the Delivery Agent."""

import sys

from delivery_agent.agent import DeliveryAgent


WELCOME = """
╔══════════════════════════════════════════════════════════════╗
║                     Delivery Agent                          ║
║  Expert in SDLC, Service Delivery, and Relationship Mgmt    ║
╚══════════════════════════════════════════════════════════════╝

Type your question or describe a situation. Commands:
  /reset  — clear conversation history
  /quit   — exit

"""


def main():
    print(WELCOME)

    agent = DeliveryAgent()

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            sys.exit(0)

        if not user_input:
            continue

        if user_input.lower() == "/quit":
            print("Goodbye!")
            sys.exit(0)

        if user_input.lower() == "/reset":
            agent.reset()
            print("[Conversation cleared]\n")
            continue

        try:
            response = agent.chat(user_input)
            print(f"\nAgent: {response}\n")
        except Exception as e:
            print(f"\n[Error: {e}]\n", file=sys.stderr)


if __name__ == "__main__":
    main()
