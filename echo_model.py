class EchoModel:
    """An echo model that returns 'You said: ' followed by the last message."""

    def reply(self, instructions, history):
        last_message = history[-1]["content"]
        return f"You said: {last_message}"
