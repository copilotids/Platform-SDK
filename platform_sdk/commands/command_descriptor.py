from typing import Optional

from pydantic import BaseModel


class EventDescriptor(BaseModel):
    """
    Describe an event that can be emitted by the Platform.
    """

    name: str
    """
    The name of the event.
    """
    payload: type[BaseModel]
    """
    The payload schema of the event.
    """


class CommandDescriptor(BaseModel):
    """
    Describe a command that can be sent to the Platform.
    """

    name: str
    """
    The name of the command.
    """
    payload: type[BaseModel]
    """
    The payload schema of the command.
    """
    result: type[BaseModel]
    """
    The result schema of the command.
    """
    exceptions: Optional[list[type[Exception]]] = None
    """
    The exceptions that can be raised when executing the command.
    None means no exceptions are expected.
    """
