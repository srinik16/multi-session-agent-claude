from claude_client import ClaudeSession
from context_classifier import detect_context

class SessionManager:

    def __init__(self):
        self.sessions = {}

    def route_session(self, user_id, question):

        context = detect_context(question)

        key = f"{user_id}:{context}"

        if key not in self.sessions:
            print(f"Creating new session for {context}")
            self.sessions[key] = ClaudeSession()

        return self.sessions[key], context


session_manager = SessionManager()
