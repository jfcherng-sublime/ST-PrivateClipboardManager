import sublime

from typing import Any, Optional, cast

from .clipboard import Clipboard
from .utils import dotted_get, dotted_set


class GlobalVariables:
    """ This class stores application-level global variables. """

    # the plugin settings object
    settings = cast(sublime.Settings, None)

    # the clipboard object
    clipboard = cast(Clipboard, None)


def global_get(dotted: str, default: Optional[Any] = None) -> Any:
    return dotted_get(GlobalVariables, dotted, default)


def global_set(dotted: str, value: Any) -> None:
    return dotted_set(GlobalVariables, dotted, value)
