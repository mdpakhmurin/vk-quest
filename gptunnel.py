from typing import Any
import aiohttp
import requests


class GPTTunnel:
    """
    Класс для взаимодействия с API GPTunnel.
    """

    def __init__(self, api_key: str):
        self._api_key = api_key
        self._assistant_url = "https://gptunnel.ru/v1/assistant/chat"
        self._completions_url = "https://gptunnel.ru/v1/chat/completions"

    async def askAssistantAsync(
        self, chatId: str, assistantCode: str, message: str
    ) -> dict[str, Any]:
        """
        Асинхронный запрос к ассистенту (см. https://docs.gptunnel.ru/assistant/chat).
        """

        headers = {"Authorization": self._api_key, "Content-Type": "application/json"}
        payload = {"chatId": chatId, "assistantCode": assistantCode, "message": message}
        async with aiohttp.ClientSession() as session:
            async with session.post(
                self._assistant_url, json=payload, headers=headers
            ) as response:
                response.raise_for_status()
                return await response.json()

    def askAssistant(
        self, chatId: str, assistantCode: str, message: str
    ) -> dict[str, Any]:
        """
        Синхронный запрос к ассистенту. (см. https://docs.gptunnel.ru/assistant/chat).
        """

        headers = {"Authorization": self._api_key, "Content-Type": "application/json"}
        payload = {"chatId": chatId, "assistantCode": assistantCode, "message": message}
        response = requests.post(self._assistant_url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    
    def complete(self, model: str, messages: list[dict]) -> dict[str, Any]:
        """
        Синхронный запрос к текстовой модели. (см. https://docs.gptunnel.ru/#node).
        """
        headers = {"Authorization": self._api_key, "Content-Type": "application/json"}
        payload = {"model": model, "messages": messages}

        response = requests.post(self._completions_url, headers=headers, json=payload)

        response.raise_for_status()
        return response.json()

    def models(self) -> dict:
        """
        Синхронный запрос к списку моделей.
        """

        headers = {"Authorization": self._api_key, "Content-Type": "application/json"}

        response = requests.get("https://gptunnel.ru/v1/models", headers=headers)
        response.raise_for_status()
        result = response.json()

        return result
