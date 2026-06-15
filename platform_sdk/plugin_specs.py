from dataclasses import dataclass
from functools import wraps
from typing import Any, Callable, Optional


@dataclass(frozen=True)
class PluginSpecifications:
    """
    Protocol defining the minimal interface for a plugin
    specification.
    """

    name: str
    """
    The name of the plugin.
    """
    version: str
    """
    The version of the plugin.
    """


def alchemy_plugin(
    specs: PluginSpecifications,
    extra_info: Optional[dict[str, Any]] = None,
) -> Callable[[Callable[[dict[str, Any]], Any]], Callable[[dict[str, Any]], Any]]:
    """
    Mark a function as the plugin entry point, providing its
    specifications and optional extra information used for plugin
    registration and management.

    :param specs: The specifications of the plugin.
    :param extra_info: Optional additional information about the plugin.
    :return: A decorator that wraps the plugin entry point function.
    """

    def decorator(
        func: Callable[[dict[str, Any]], Any],
    ) -> Callable[[dict[str, Any]], Any]:
        # Preserves the original function's name and docstring
        @wraps(func)
        def wrapper(
            params: dict[str, Any],
        ) -> tuple[Any, PluginSpecifications, Optional[dict[str, Any]]]:
            return func(params), specs, extra_info

        return wrapper

    return decorator
