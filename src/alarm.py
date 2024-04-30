"""
This module contains some alarm system,
currently we have TG chatbot.
"""

import requests
import os


class TGBot:
    """
    Telegram chatbot.
    """

    def __init__(self) -> None:
        self.token = os.getenv("tg_token")
        self.chat_id = os.getenv("tg_chat_id")

    def send_message(self, text: str):
        """
        Send message.

        Args:
            text (str): text you want to send.

        Returns:
            response.
        """
        return requests.get(
            url=f'https://api.telegram.org/bot{self.token}/sendMessage?chat_id={self.chat_id}&text={text}',
            timeout=60
        )
