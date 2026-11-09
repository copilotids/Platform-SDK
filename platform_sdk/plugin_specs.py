from dataclasses import dataclass
from functools import wraps
from typing import Any, Callable, Literal, Optional, Sequence


@dataclass(frozen=True, kw_only=True)
class LLMConfig:
    """Configuration for the language model used in the assistant chat."""

    llm_name: str
    """The name of the language model."""
    effort: Optional[Sequence[str]] = None
    """The effort level supported by the language model, if applicable."""


def alchemy_plugin(
    plugin_name: str,
    plugin_version: str,
    extra_info: Optional[dict[str, Any]] = None,
    supported_llm: Optional[
        dict[Literal["coordinator", "subagent"], Sequence[LLMConfig]]
    ] = None,
) -> Callable[[Callable[[dict[str, Any]], Any]], Callable[[dict[str, Any]], Any]]:
    """
    Mark a function as the plugin entry point, providing its
    specifications and optional extra information used for
    plugin registration and management.

    :param plugin_name: The name of the plugin.
    :param plugin_version: The version of the plugin.
    :param extra_info: Optional additional information about the plugin.
    :param supported_llm: Optional dictionary specifying the supported
        language models for the plugin, with keys "coordinator" and "subagent"
        mapping to their respective LLMConfig instances.
    :return: A decorator that wraps the plugin entry point function
        and returns its output along with the plugin
        specifications and extra information.
    """

    def decorator(
        func: Callable[[dict[str, Any]], Any],
    ) -> Callable[[dict[str, Any]], Any]:

        @wraps(func)
        def wrapper(
            params: dict[str, Any],
        ) -> tuple[Any, str, str, Optional[dict[str, Any]]]:
            return func(params), plugin_name, plugin_version, extra_info

        return wrapper

    return decorator
