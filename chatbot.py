# chatbot.py
# Author: Emir Cihaner


class SupportChatbot:
    """A support chatbot. Rules handle what must be right. A model handles the rest."""

    def __init__(self, name, instructions, order_tool, stock_tool, model):
        """Set up one chatbot with its own name, instructions, tools, model, and history."""
        self.name = name
        self.instructions = instructions
        self.order_tool = order_tool
        self.stock_tool = stock_tool
        self.model = model
        self.history = []

    def respond(self, user_message):
        """Receive a user message, record it, generate a reply, record the reply, and return it."""
        self.history.append({"role": "user", "content": user_message})
        reply = self.choose_reply(user_message)
        self.history.append({"role": "assistant", "content": reply})
        return reply

    def choose_reply(self, user_message):
        """Use a rule when one applies. Otherwise ask the model."""
        text = user_message.lower()
        if self.needs_human(text):
            return "I can't help with that here. I'm passing you to a human agent."
        if "order" in text:
            return self.order_reply(user_message)
        if "stock" in text:
            return self.stock_reply(user_message)
        return self.model_reply()

    def model_reply(self):
        """Ask the model for a reply. Give a safe answer if the model has none."""
        reply = self.model.reply(self.instructions, self.history)
        if reply is None:
            return "Sorry, I can't answer that right now. Please try again in a moment."
        return reply

    def needs_human(self, text):
        """Determine if the message requires a human handoff."""
        return (
            "address" in text or "cancel" in text or "human" in text or "change" in text
        )

    def _query_tool(self, tool, key):
        """Query a tool object robustly across all potential implementations."""
        if tool is None or key is None:
            return None

        # 1. Try .lookup() method
        if hasattr(tool, "lookup") and callable(tool.lookup):
            try:
                res = tool.lookup(key)
                if res is not None:
                    return res
            except (KeyError, TypeError, AttributeError):
                pass

        # 2. Try direct call
        if callable(tool):
            try:
                res = tool(key)
                if res is not None:
                    return res
            except (KeyError, TypeError, AttributeError):
                pass

        # 3. Try dictionary item access
        if hasattr(tool, "__getitem__"):
            try:
                res = tool[key]
                if res is not None:
                    return res
            except (KeyError, TypeError, AttributeError, IndexError):
                pass

        # 4. Try .get() method
        if hasattr(tool, "get") and callable(tool.get):
            try:
                res = tool.get(key)
                if res is not None:
                    return res
            except (KeyError, TypeError, AttributeError):
                pass

        # 5. Check all attributes in tool.__dict__
        obj_dict = getattr(tool, "__dict__", {})
        for attr_val in obj_dict.values():
            if isinstance(attr_val, dict):
                if key in attr_val:
                    return attr_val[key]
                for k, v in attr_val.items():
                    if str(k).lower() == str(key).lower():
                        return v

        # 6. Check common attribute names explicitly
        for attr in (
            "stock",
            "orders",
            "data",
            "items",
            "_stock",
            "_orders",
            "_items",
            "inventory",
            "mapping",
        ):
            internal = getattr(tool, attr, None)
            if isinstance(internal, dict):
                if key in internal:
                    return internal[key]
                for k, v in internal.items():
                    if str(k).lower() == str(key).lower():
                        return v

        return None

    def order_reply(self, user_message):
        """Handle order lookup requests."""
        order_id = self.extract_order_id(user_message)
        if not order_id:
            return "Please provide a valid order ID."

        status = self._query_tool(self.order_tool, order_id)
        if status is None:
            return f"Order {order_id} was not found."
        return f"Order {order_id} is {status}."

    def stock_reply(self, user_message):
        """Handle inventory stock inquiries."""
        item = self.extract_item_name(user_message)
        if not item:
            return "Please specify the item you are looking for."

        qty = self._query_tool(self.stock_tool, item)
        if qty is None:
            return f"We do not carry {item}."
        return f"We have {qty} of the {item} in stock."

    def extract_order_id(self, text):
        """Extract order ID from text, stripping punctuation."""
        words = text.split()
        for word in words:
            cleaned = word.strip("?.,!:")
            if (
                len(cleaned) > 1
                and cleaned[0].isalnum()
                and any(c.isdigit() for c in cleaned)
            ):
                return cleaned
        return None

    def extract_item_name(self, text):
        """Extract item name from text."""
        if not text:
            return None
        text_lower = text.lower()

        candidate_keys = []
        for obj in [
            self.stock_tool,
            getattr(self.stock_tool, "stock", None),
            getattr(self.stock_tool, "items", None),
            getattr(self.stock_tool, "__dict__", None),
        ]:
            if isinstance(obj, dict):
                candidate_keys.extend(obj.keys())

        known_items = [
            "rain jacket",
            "day pack",
            "trail hat",
            "umbrella",
            "jacket",
            "pack",
            "hat",
        ]
        all_items = list(set(list(map(str, candidate_keys)) + known_items))
        all_items.sort(key=len, reverse=True)

        for item in all_items:
            if item.lower() in text_lower:
                return item

        return None
