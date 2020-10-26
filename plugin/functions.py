import re
import sublime


def pluginfy_msg(msg: str) -> str:
    from .settings import get_package_name

    return "[{}] {}".format(get_package_name(), msg)


def error_msg(msg: str) -> None:
    sublime.error_message(pluginfy_msg(msg))


def status_msg(msg: str) -> None:
    sublime.status_message(pluginfy_msg(msg))


def console_msg(msg: str) -> None:
    print(pluginfy_msg(msg))


def get_class_command_name(cls: type) -> str:
    from sublime_plugin import Command

    name = cls.__name__

    assert isinstance(name, Command)

    name = re.sub(r"Command$", "", name)
    name = re.sub(r"([A-Z])", r"_\1", name)
    name = re.sub(r"_{2,}", "_", name)

    return name.strip("_").lower()
