from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Optional

from pydantic import BaseModel

from .i_assistant_chat import AssistantChat, AssistantMessage


@dataclass(frozen=True, kw_only=True)
class ChosenLLM:
    """The LLM chosen to handle a specific request."""

    llm_name: str
    """The name of the language model."""
    effort: Optional[str] = None
    """The effort level for the language model, if applicable."""


@dataclass(frozen=True)
class AssistantSpecifications:
    """Protocol defining the minimal interface for an assistant specification."""

    name: str
    """The name of the assistant."""
    version: str
    """The version of the assistant."""


class Assistant(ABC):
    """
    Protocol defining the minimal interface an assistant must implement in order to
    be used within the Platform.

    An assistant relies on a knowledge model to process requests and provide answers.
    The model is based on Pydantic ``BaseModel``, allowing for structured data
    handling and validation.
    """

    @property
    @abstractmethod
    def specifications(self) -> AssistantSpecifications:
        """:return: The assistant specifications."""

    @property
    @abstractmethod
    async def get_model(self) -> BaseModel:
        """:return: The current assistant knowledge model."""

    @abstractmethod
    async def set_model(self, model: BaseModel) -> None:
        """
        Change the current assistant knowledge model.

        :param model: The assistant model to set.
        """

    @abstractmethod
    async def export_model(self) -> tuple[Any, str]:
        """
        Export the assistant knowledge model asynchronously
        without blocking the assistant invocation.

        :return: The exported model and its extension.
        """

    @abstractmethod
    async def invoke(
        self,
        request: str | AssistantChat,
        request_additional_info: Optional[dict[str, Any]] = None,
        models_to_use: Optional[dict[str, ChosenLLM]] = None,
    ) -> AssistantMessage:
        """
        Invoke the assistant on the provided request.

        :param request: The user request or the full chat history,
            where the user's current request is included as the final
            message.
        :param request_additional_info: Additional information to be used when
            processing the request (e.g., user profile, web pages, ...).
            The assistant could ignore this data if not relevant.
        :param models_to_use: Optional dictionary mapping roles to the chosen LLMs
            for handling the request.
            If None, default LLM for each role will be used.
        :return: The assistant response.
        """
