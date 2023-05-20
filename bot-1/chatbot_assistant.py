import openai
import os
from dotenv import load_dotenv, find_dotenv
from typing import List


class ChatMessage:
    """
    Represents a single message in the conversation.
    """

    def __init__(self, role: str, content: str):
        """
        :param role: The role of the message sender (e.g. 'user', 'assistant', etc.)
        :param content: The content of the message
        """
        self.role = role
        self.content = content


class ChatbotAssistant:
    """
    A chatbot assistant that uses OpenAI's GPT-3 to generate responses to user input.
    """

    def __init__(self, system_prompt: str):
        """
        :param system_prompt: The initial prompt to display to the user
        """
        self.system_prompt = system_prompt
        self.api_key = self._load_api_key()

    def _load_api_key(self) -> str:
        """
        Load the OpenAI API key from the environment variables.
        """
        _ = load_dotenv(find_dotenv())
        return os.getenv("OPENAI_API_KEY")

    def get_chatbot_response(
        self,
        messages: List[ChatMessage],
        model: str = "gpt-3.5-turbo",
        temperature: float = 0.5,
    ) -> str:
        """
        Get a response from the OpenAI model for a given conversation history.

        :param messages: The conversation history as a list of ChatMessage objects
        :param model: The OpenAI model to use
        :param temperature: The temperature for controlling randomness
        :return: The model's response as a string
        """
        openai.api_key = self.api_key
        formatted_messages = [
            {"role": message.role, "content": message.content} for message in messages
        ]
        response = openai.ChatCompletion.create(
            model=model,
            messages=formatted_messages,
            temperature=temperature,
        )
        return response.choices[0].message["content"]
