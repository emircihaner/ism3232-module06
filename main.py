# main.py
# Author: [Emir Cihaner]

from chatbot import SupportChatbot
from order_tool import OrderLookup
from stock_tool import StockLookup


def make_bot():
    orders = {"A100": "shipped", "A101": "processing"}
    stock = {"rain jacket": 12}
    return SupportChatbot(
        "Sunny",
        "You are cheerful and brief.",
        OrderLookup(orders),
        StockLookup(stock),
    )


def main():
    bot = make_bot()
    print("Type a message, or type quit to stop.")
    while True:
        try:
            user_input = input("You: ")
        except EOFError:
            break
        if user_input.strip().lower() == "quit":
            break
        reply = bot.respond(user_input)
        print(f"{bot.name}: {reply}")

    print(f"Messages in this conversation: {len(bot.history)}")


if __name__ == "__main__":
    main()