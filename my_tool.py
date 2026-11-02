# my_tool.py


class AppointmentLookup:
    """A tool that manages open appointment times."""

    def __init__(self, schedule):
        self.schedule = schedule

    def find_day(self, text):
        text_lower = text.lower()
        for day in self.schedule:
            if day in text_lower:
                return day
        return None

    def get_times(self, day):
        return self.schedule.get(day)
