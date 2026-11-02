# my_main.py
from my_assistant import AppointmentAssistant
from my_tool import AppointmentLookup


def main():
    schedule = {
        "monday": ["9:00 am", "2:30 pm"],
        "wednesday": ["10:00 am", "3:00 pm"],
        "friday": ["11:00 am", "4:00 pm"],
    }
    tool = AppointmentLookup(schedule)
    robin = AppointmentAssistant("Robin", "Help people find appointment times.", tool)

    print("Type a message, or type quit to stop.")
    while True:
        try:
            user_input = input("You: ")
        except EOFError:
            break
        if user_input.strip().lower() == "quit":
            break
        reply = robin.respond(user_input)
        print(f"Robin: {reply}")

    print(f"Messages in this conversation: {len(robin.history)}")


if __name__ == "__main__":
    main()
