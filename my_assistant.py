# my_assistant.py


class AppointmentAssistant:
    """An assistant that helps users find open appointment slots."""

    def __init__(self, name, instructions, appointment_tool):
        self.name = name
        self.instructions = instructions
        self.appointment_tool = appointment_tool
        self.history = []

    def respond(self, user_message):
        self.history.append({"role": "user", "content": user_message})
        reply = self.choose_reply(user_message)
        self.history.append({"role": "assistant", "content": reply})
        return reply

    def choose_reply(self, user_message):
        text = user_message.lower()
        if "book" in text or "schedule" in text or "change" in text:
            return "I can't change the schedule. I'm passing you to the front desk."
        if "hello" in text or "hi" in text:
            return f"Hello! I'm {self.name}. Ask me which times are open on a day."

        day = self.appointment_tool.find_day(text)
        if day:
            times = self.appointment_tool.get_times(day)
            times_str = " and ".join(times)
            return f"Open times on {day}: {times_str}."

        if "available" in text or "open" in text:
            return "Which day? I can check Monday, Wednesday, or Friday."

        return "I'm not sure how to help with that. I can list open times."
