from abc import ABC, abstractmethod
from typing import Any, Sequence

from .command_descriptor import CommandDescriptor


class ICommandGateway(ABC):
    """
    Abstract base class defining the interface for a command gateway
    that allows the communication with the Alchemy Platform from
    external systems.
    """

    @abstractmethod
    def dispatch_command(
        self,
        name: str,
        payload: Any,
        producer_id: str,
        generator_id: str,
        transaction_id: str | None = None,
    ) -> None:
        """
        Dispatch a command to the Platform and forget about its result.

        :param name: The name of the command to be dispatched.
        :param payload: The payload of the command.
        :param producer_id: The identifier of the producer dispatching
            the command.
        :param generator_id: The identifier of the generator of
            the command.
        :param transaction_id: Optional identifier of the transaction
            to which the command belongs.
        """

    @abstractmethod
    async def dispatch_and_await_result(
        self,
        name: str,
        payload: Any,
        producer_id: str,
        generator_id: str,
        transaction_id: str | None = None,
    ) -> Any:
        """
        Dispatch a command to the Platform and await its result.

        :param name: The name of the command to be dispatched.
        :param payload: The payload of the command.
        :param producer_id: The identifier of the producer dispatching
            the command.
        :param generator_id: The identifier of the generator of the command.
        :param transaction_id: Optional identifier of the transaction
            to which the command belongs.
        :return: The result of the command.
        """

    @property
    @abstractmethod
    def available_commands(self) -> Sequence[CommandDescriptor]:
        """
        Get all available commands the Platform can process.

        :return: The available commands.
        """
