# two_bots.py
from chatbot import SupportChatbot
from order_tool import OrderLookup
from stock_tool import StockLookup

order_tool = OrderLookup({"A100": "shipped", "A101": "processing"})
stock_tool = StockLookup({"rain jacket": 12})

sunny = SupportChatbot(
    "Sunny", "You are cheerful and brief.", order_tool, stock_tool
)
river = SupportChatbot(
    "River", "You are formal and detailed.", order_tool, stock_tool
)

sunny_reply1 = sunny.respond("hello")
sunny.respond("Where is order A100?")

river_reply1 = river.respond("hello")

print(f"{sunny.name} {len(sunny.history)}")
print(f"{river.name} {len(river.history)}")
print(sunny_reply1)
print(river_reply1)
print(sunny.instructions)
print(river.instructions)