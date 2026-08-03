from abc import ABC, abstractmethod
from typing import Any, Awaitable, Callable, Optional, Sequence

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
        handler: Callable[[Any], Awaitable[None] | None],
        filter_by_names: Optional[set[str]] = None,
    ) -> None:
        """
        Listen to an event emitted by the Platform and
        invoke the handler.

        :param handler: The handler to be called when the event
            is received.
            It can be a coroutine or a synchronous function.
        :param filter_by_names: The names of the events to listen to.
            If None, all events will be listened to.
        """

    @abstractmethod
    async def await_event(
        self,
        event_filter: Callable[[Any], bool],
        timeout_seconds: float,
    ) -> object:
        """
        Await an event emitted by the Platform that matches the
        `event_filter`.

        :param event_filter: A callable that takes an event and
            returns True if the event matches the filter,
            False otherwise.
        :param timeout_seconds: The maximum seconds (> 0) to wait for
            the event.
        :return: The event that matches the filter.
        :raises TimeoutError: If the event is not received within
            the timeout.
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
