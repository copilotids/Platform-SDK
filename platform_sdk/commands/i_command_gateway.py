from abc import ABC, abstractmethod
from typing import Any, Callable, Optional, Sequence

from .command_descriptor import CommandDescriptor, EventDescriptor


class CommandGateway(ABC):
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

    # Events

    @abstractmethod
    def listen_to_event(
        self,
        name: Optional[str],
        handler: Callable[[Any], None],
    ) -> None:
        """
        Listen to an event emitted by the Platform.

        :param name: The name of the event to listen to.
            If None, listen to all events.
        :param handler: The handler to be called when the event
            is emitted.
        """

    @abstractmethod
    async def await_event(
        self, handler: Callable[[Any], bool], timeout: float
    ) -> object:
        """
        Await an event emitted by the Platform.

        :param handler: The handler to be called when the event is emitted.
            It should return True if the event is the one we are
            waiting for, False otherwise.
        :param timeout: The maximum seconds to wait for the event.
        :return: The event.
        :raises TimeoutError: If the event is not emitted within the timeout.
        """

    # Commands

    @abstractmethod
    def dispatch_command(
        self,
        name: str,
        payload: Any,
        producer_id: str,
        generator_id: str,
        transaction_id: Optional[str] = None,
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
    async def dispatch_command_and_await_result(
        self,
        name: str,
        payload: Any,
        producer_id: str,
        generator_id: str,
        transaction_id: Optional[str] = None,
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
        :return: The command result or an exception according to the
            command definition.
        """
