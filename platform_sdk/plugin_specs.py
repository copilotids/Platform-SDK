from dataclasses import dataclass, field
from functools import wraps
from typing import Any, Callable, Mapping, Optional, Sequence


@dataclass(frozen=True, kw_only=True)
class Role:
    """The role the LLM may play in the plugin, such as "coordinator" or "subagent"."""

    name: str
    """The name of the role."""
    description: Optional[str] = field(default=None, compare=False)
    """Optional description of the role (excluded from the hash)."""


@dataclass(frozen=True, kw_only=True)
class SupportedLLM:
    """An LLM supported by a plugin for a specific role."""

    llm_name: str
    """The name of the language model."""
    effort: Optional[Sequence[str]] = None
    """The effort level supported by the language model, if applicable."""


RoleMap = Optional[Mapping[Role, Sequence[SupportedLLM]]]
ExtraInfo = Optional[Mapping[str, Any]]


def alchemy_plugin(
    plugin_name: str,
    plugin_version: str,
    supported_models: RoleMap = None,
    extra_info: ExtraInfo = None,
) -> Callable[[Callable[[dict[str, Any]], Any]], Callable[[dict[str, Any]], Any]]:
    """
    Mark a function as the plugin entry point, providing its specifications and
    optional extra information used for plugin registration and management.

    :param plugin_name: The name of the plugin.
    :param plugin_version: The version of the plugin.
    :param supported_models: Optional dictionary mapping roles to their supported
        language models (LLMs).
    :param extra_info: Optional additional information about the plugin.
    :return: A decorator that wraps the plugin entry point function
        and returns its output with the plugin specifications, supported models,
        and extra information.
    """

    def decorator(
        func: Callable[[dict[str, Any]], Any],
    ) -> Callable[[dict[str, Any]], Any]:

        @wraps(func)
        def wrapper(
            params: dict[str, Any],
        ) -> tuple[Any, str, str, RoleMap, ExtraInfo]:
            return (
                func(params),
                plugin_name,
                plugin_version,
                supported_models,
                extra_info,
            )

        return wrapper

    return decorator
