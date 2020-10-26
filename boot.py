import sublime
import sys

from .plugin.functions import pluginfy_msg
from .plugin.settings import get_package_name


PLUGIN_NAME = "PrivateClipboardManager"

if int(sublime.version()) < 4085:
    raise RuntimeError(pluginfy_msg("This plugin only runs on ST >= 4085"))

if sys.version_info[:3] < (3, 8, 0):
    raise RuntimeError(pluginfy_msg("This plugin only runs on Python >= 3.8"))

if get_package_name() != PLUGIN_NAME:
    raise RuntimeError(pluginfy_msg(f"This plugin must be put in `{PLUGIN_NAME}` directory"))

from .plugin import *


def plugin_loaded() -> None:
    set_up()


def plugin_unloaded() -> None:
    tear_down()
