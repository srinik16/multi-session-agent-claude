from anthropic import Anthropic
from dotenv import load_dotenv
import os

load_dotenv()


class ClaudeSession:

    def __init__(self):
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.history = []

    def ask(self, question: str) -> str:
        self.history.append({"role": "user", "content": question})

        response = self.client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=1024,
            messages=self.history
        )

        answer = response.content[0].text
        self.history.append({"role": "assistant", "content": answer})

        return answer
