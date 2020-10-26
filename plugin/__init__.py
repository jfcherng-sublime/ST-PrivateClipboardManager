from .clipboard import Clipboard
from .globals import global_get, global_set
from .private_clipboard_manager import (
    PrivateClipboardManagerCommand,
    PrivateClipboardManagerPasteCommand,
)
from .settings import get_package_name, get_setting, get_settings_object


__all__ = [
    "set_up",
    "tear_down",
    # ST command classes
    "PrivateClipboardManagerCommand",
    "PrivateClipboardManagerPasteCommand",
]


def set_up() -> None:
    """ plugin_loaded """

    # init global objects
    global_set("settings", get_settings_object())
    global_set("clipboard", Clipboard())

    settings_listener()
    get_settings_object().add_on_change(get_package_name(), settings_listener)


def tear_down() -> None:
    """ plugin_unloaded """

    get_settings_object().clear_on_change(get_package_name())


def settings_listener() -> None:
    clipboard = global_get("clipboard")
    clipboard.capacity = get_setting("clipboard_capacity")
