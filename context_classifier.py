from anthropic import Anthropic
from dotenv import load_dotenv
import os

load_dotenv()
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

def detect_context(question: str):

    prompt = f"""
Classify the user question into a short context name.

Rules:
- one or two words only
- lowercase
- no explanation

Examples:
"What is Python?" -> coding
"Best hotels in Paris?" -> travel
"How to invest money?" -> finance

Question:
{question}
"""

    response = client.messages.create(
        model="claude-haiku-4-5-20251001",  # cheaper + fast
        max_tokens=10,
        messages=[{"role": "user", "content": prompt}]
    )

    return response.content[0].text.strip()
