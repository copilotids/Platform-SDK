"""
Interoperability API between AI assistants and the
Alchemy platform.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from pydantic import BaseModel

from .i_assistant_chat import IAssistantChat


@dataclass(frozen=True)
class AssistantSpecifications:
    """
    Protocol defining the minimal interface for an AI assistant
    specification.
    """

    name: str
    """
    The name of the assistant.
    """
    version: str
    """
    The version of the assistant.
    """
    chat_model_name: str
    """
    The name of the LLM used by the assistant.
    """


class IAssistant(ABC):
    """
    Protocol defining the minimal interface an AI assistant must
    implement in order to be used within the Platform.

    An AI assistant relies on a knowledge model to process requests
    and provide answers.
    The model is represented as a Pydantic BaseModel, allowing for
    structured data handling and validation.
    """

    @abstractmethod
    async def invoke(
        self,
        request: str | IAssistantChat,
        request_contextual_data: dict[str, Any] | None,
    ) -> tuple[str, BaseModel, BaseModel]:
        """
        Invoke the assistant on the provided request.

        :param request: The request to process, either as a
            simple string or as the full chat history including the request.
        :param request_contextual_data: Additional information to be used when
            processing the request (e.g., user profile information, system
            state, etc.). The assistant can choose to ignore this data if
            not relevant for the request processing.
        :return: A tuple containing the assistant response,
            the model before the execution, and the model after the execution.
        """

    @abstractmethod
    async def set_model(self, model: BaseModel) -> None:
        """
        Change the current assistant knowledge model.

        :param model: The assistant model to set.
        """

    @property
    @abstractmethod
    async def get_model(self) -> BaseModel:
        """
        :return: The current assistant knowledge model.
        """

    @abstractmethod
    async def export_model(self) -> tuple[Any, str]:
        """
        Export the assistant knowledge model asynchronously
        (without blocking the assistant invocation).

        :return: A tuple containing the exported model and its
            extension.
        """

    @property
    @abstractmethod
    def specifications(self) -> AssistantSpecifications:
        """
        :return: The assistant specifications.
        """
