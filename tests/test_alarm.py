import os

import requests_mock

from src.alarm import TGBot


def test_openai_agent():
    with requests_mock.Mocker() as m:
        os.environ["tg_token"] = "123"
        os.environ["tg_chat_id"] = "123"
        text = "123"

        m.get(
            'https://api.telegram.org/bot123/sendMessage?chat_id=123&text=123',
            text='{"response":"ok"}')

        tg_bot = TGBot()
        assert tg_bot.send_message(text).status_code == 200
