from functools import wraps
from typing import Any, Callable, Optional


def alchemy_plugin(
    plugin_name: str,
    plugin_version: str,
    extra_info: Optional[dict[str, Any]] = None,
) -> Callable[[Callable[[dict[str, Any]], Any]], Callable[[dict[str, Any]], Any]]:
    """
    Mark a function as the plugin entry point, providing its
    specifications and optional extra information used for
    plugin registration and management.

    :param plugin_name: The name of the plugin.
    :param plugin_version: The version of the plugin.
    :param extra_info: Optional additional information about the plugin.
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
