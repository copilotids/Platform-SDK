from typing import Optional

from pydantic import BaseModel, Field


class EventDescriptor(BaseModel):
    """
    Describe an event that can be emitted by the Platform.
    """

    name: str = Field(
        ...,
        description="The name of the event.",
    )
    payload: Optional[type[BaseModel]] = Field(
        default=None,
        description=(
            "The schema of the event payload. "
            "If None, the event does not have a payload."
        ),
    )


class CommandDescriptor(BaseModel):
    """
    Describe a command that can be sent to the Platform.
    """

    name: str = Field(
        ...,
        description="The name of the command.",
    )
    payload: Optional[type[BaseModel]] = Field(
        default=None,
        description=(
            "The schema of the command payload. "
            "If None, the command does not require a payload."
        ),
    )
    result: Optional[type[BaseModel]] = Field(
        default=None,
        description=(
            "The schema of the command result. "
            "If None, the command does not return a result."
        ),
    )
    exceptions: Optional[list[type[Exception]]] = Field(
        default=None,
        description=(
            "The exceptions that can be raised when executing "
            "the command. "
            "If None, the command does not raise any exception."
        ),
    )
