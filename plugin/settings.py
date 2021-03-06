import os
import sublime
import tempfile
import time

from typing import Any, Dict, Optional


def get_package_name() -> str:
    """
    @brief Getsthe package name.

    @return The package name.
    """

    # __package__ will be "THE_PLUGIN_NAME.plugin" under this folder structure
    # anyway, the top module should always be the plugin name
    return __package__.partition(".")[0]


def get_package_path() -> str:
    """
    @brief Gets the package path.

    @return The package path.
    """

    return "Packages/" + get_package_name()


def get_expanding_variables(window: Optional[sublime.Window]) -> Dict[str, Any]:
    variables = {
        "home": os.path.expanduser("~"),
        "package_name": get_package_name(),
        "package_path": get_package_path(),
        "temp_dir": tempfile.gettempdir(),
    }

    if window:
        variables.update(window.extract_variables())

    return variables


def get_settings_file() -> str:
    """
    @brief Get the settings file name.

    @return The settings file name.
    """

    return get_package_name() + ".sublime-settings"


def get_settings_object() -> sublime.Settings:
    """
    @brief Get the plugin settings object. This function will call `sublime.load_settings()`.

    @return The settings object.
    """

    return sublime.load_settings(get_settings_file())


def get_setting(dotted: str, default: Optional[Any] = None) -> Any:
    """
    @brief Get the plugin setting with the dotted key.

    @param dotted  The dotted key
    @param default The default value if the key doesn't exist

    @return The setting's value.
    """

    from .globals import global_get

    return global_get(f"settings.{dotted}", default)


def get_timestamp() -> float:
    """
    @brief Get the current timestamp (in second).

    @return The timestamp.
    """

    return time.time()
