# tests/test_my_assistant.py
from my_assistant import AppointmentAssistant
from my_tool import AppointmentLookup


def make_assistant():
    schedule = {"monday": ["9:00 am"]}
    return AppointmentAssistant(
        "Robin", "Help with appointments.", AppointmentLookup(schedule)
    )


def test_tool_finds_day():
    tool = AppointmentLookup({"monday": ["9:00 am"]})
    assert tool.find_day("What is open on Monday?") == "monday"


def test_assistant_greets():
    bot = make_assistant()
    assert "Hello" in bot.respond("hello")


def test_assistant_uses_tool():
    bot = make_assistant()
    assert "9:00 am" in bot.respond("What times on monday?")


def test_assistant_handoff_to_human():
    bot = make_assistant()
    assert "front desk" in bot.respond("Please book me for Monday")
