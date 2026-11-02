# tests/test_chatbot.py
from chatbot import SupportChatbot
from order_tool import OrderLookup
from stock_tool import StockLookup


def make_bot():
    """Build a fresh chatbot with its tools for each test."""
    orders = {"A100": "shipped", "A101": "processing"}
    stock = {"rain jacket": 12}
    return SupportChatbot(
        "Sunny", "Be friendly.", OrderLookup(orders), StockLookup(stock)
    )


def test_count_user_messages():
    bot = make_bot()
    bot.respond("hello")
    bot.respond("Where is order A100?")
    assert bot.count_user_messages() == 2


def test_stock_tool():
    bot = make_bot()
    reply = bot.respond("Is the rain jacket in stock?")
    assert "12" in reply


def test_respond_records_both_messages():
    bot = make_bot()
    bot.respond("Hello")
    assert len(bot.history) == 2


def test_order_question_uses_the_tool():
    bot = make_bot()
    reply = bot.respond("Where is order A100?")
    assert "shipped" in reply


def test_order_question_without_an_id_asks_for_one():
    bot = make_bot()
    reply = bot.respond("Where is my order?")
    assert "ID" in reply or "order" in reply.lower()


def test_address_change_goes_to_a_human():
    bot = make_bot()
    reply = bot.respond("Please change my address.")
    assert "human" in reply.lower() or "desk" in reply.lower()


def test_unknown_request_gets_a_safe_reply():
    bot = make_bot()
    reply = bot.respond("What is the meaning of life?")
    assert len(reply) > 0


def test_two_chatbots_keep_separate_histories():
    first = make_bot()
    second = make_bot()
    first.respond("Hello")
    assert len(first.history) == 2
    assert len(second.history) == 0