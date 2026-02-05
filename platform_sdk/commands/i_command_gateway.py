from abc import ABC, abstractmethod
from typing import Any, Sequence

from .command_descriptor import CommandDescriptor, EventDescriptor


class ICommandGateway(ABC):
    """
    Command gateway definition.
    It allows the communication with the Alchemy Platform from
    external systems.
    """

    @property
    @abstractmethod
    def available_commands(self) -> Sequence[CommandDescriptor]:
        """
        Get all available commands the Platform can process.

        :return: The available commands.
        """

    @property
    @abstractmethod
    def available_events(self) -> Sequence[EventDescriptor]:
        """
        Get all available events the Platform can emit.

        :return: The available events.
        """

    @abstractmethod
    def dispatch_command(
        self,
        name: str,
        payload: Any,
        producer_id: str,
        generator_id: str,
        transaction_id: str | None = None,
        broadcast: bool = False,
    ) -> None:
        """
        Dispatch a command to the right Platform handler
        and forget about its result.

        Details:
            - Asynchronous operation with no result expected.
            - The command can be broadcasted to all handlers
              running in the Platform.

        :param name: The name of the command to be dispatched.
        :param payload: The payload of the command.
        :param producer_id: The identifier of the producer dispatching
            the command.
        :param generator_id: The identifier of the generator of
            the command.
        :param transaction_id: Optional identifier of the transaction
            to which the command belongs.
        :param broadcast: Whether to broadcast the command to all handlers.
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
