import enum
import sublime
import sublime_plugin

from typing import Any, Dict

from .clipboard import Clipboard, ClipboardItem
from .functions import (
    console_msg,
    error_msg,
    get_class_command_name,
    status_msg,
)
from .settings import get_setting
from .utils import repeat_iterable


def get_clipboard() -> Clipboard:
    """ Gets the clipboard object. """

    from .globals import global_get

    clipboard = global_get("clipboard")

    if not isinstance(clipboard, Clipboard):
        console_msg("The clipboard object is not ready yet. Try again later...")

    return clipboard


class ManagerOperations(enum.IntEnum):
    clear = enum.auto()
    copy = enum.auto()
    cut = enum.auto()
    debug = enum.auto()
    paste = enum.auto()


class PrivateClipboardManagerCommand(sublime_plugin.TextCommand):
    def is_visible(self) -> bool:
        return False

    def run(self, edit: sublime.Edit, operation: str, args: Dict[str, Any] = {}) -> None:  # type: ignore
        clipboard = get_clipboard()

        try:
            m_op = ManagerOperations[operation]

            if m_op == ManagerOperations.debug:
                return self._do_debug(clipboard, args=args)

            if m_op == ManagerOperations.copy or m_op == ManagerOperations.cut:
                return self._do_copy_or_cut(clipboard, edit, m_op, args=args)

            if m_op == ManagerOperations.paste:
                return self._do_paste(clipboard, args=args)

            if m_op == ManagerOperations.clear:
                return self._do_clear(clipboard, args=args)

        except (KeyError, ValueError):
            error_msg(f"Unknown operation: {operation}")

    def _do_copy_or_cut(
        self, clipboard: Clipboard, edit: sublime.Edit, m_op: ManagerOperations, args: Dict[str, Any] = {},
    ) -> None:
        sel = self.view.sel()

        if len(sel) < 1:
            return

        texts = [self.view.substr(r) for r in sel]

        # requirement: at least one selection has text
        if not any(texts):
            return status_msg("No valid text...")

        clipboard.add_texts(texts)

        if m_op == ManagerOperations.copy:
            status_msg("Text copied!")
        elif m_op == ManagerOperations.cut:
            status_msg("Text cut!")

            for r in sel:
                self.view.replace(edit, r, "")

    def _do_paste(self, clipboard: Clipboard, args: Dict[str, Any] = {}) -> None:
        def run_paste_command(view: sublime.View, args: Dict[str, Any] = {}) -> None:
            view.run_command(get_class_command_name(PrivateClipboardManagerPasteCommand), {"args": args})

        def create_panel_item(view: sublime.View, item: ClipboardItem) -> sublime.QuickPanelItem:
            return sublime.QuickPanelItem(
                kind=(
                    (sublime.KIND_ID_MARKUP, get_setting("sign_item_applicable"), "")
                    if item.appliable_to_selection(view.sel())
                    else (sublime.KIND_ID_AMBIGUOUS, get_setting("sign_item_inapplicable"), "")
                ),
                trigger=get_setting("caret_texts_delimiter").join(item.texts),
                annotation=f"(carets = {len(item.texts)})",
            )

        if "nth" in args:
            return run_paste_command(self.view, args)

        panel_items = clipboard.get_sorted_items()

        self.view.window().show_quick_panel(  # type: ignore
            [create_panel_item(self.view, item) for item in reversed(panel_items)],
            on_select=lambda idx: run_paste_command(
                self.view,
                {
                    **args,
                    # ...
                    "nth": None if idx == -1 else len(panel_items) - (idx + 1),
                },
            ),
            placeholder="Choose the text to be pasted...",
        )

    def _do_clear(self, clipboard: Clipboard, args: Dict[str, Any] = {}) -> None:
        clipboard.clear()

        status_msg("All items have been deleted!")

    def _do_debug(self, clipboard: Clipboard, args: Dict[str, Any] = {}) -> None:
        console_msg(f"Clipboard information: {clipboard!r}")


class PrivateClipboardManagerPasteCommand(sublime_plugin.TextCommand):
    def is_visible(self) -> bool:
        return False

    def run(self, edit: sublime.Edit, args: Dict[str, Any] = {}) -> None:  # type: ignore
        clipboard = get_clipboard()

        if "nth" in args and args["nth"] is None:
            return

        # paste the latest item by default
        nth = int(args.setdefault("nth", -1))
        promote_pasted_item = bool(args.setdefault("promote_pasted_item", get_setting("promote_pasted_item")))

        if len(clipboard) == 0:
            return status_msg("Clipboard is empty...")

        try:
            item = clipboard[nth]
        except IndexError:
            return status_msg(f"Paste `nth` out of bound: {nth}")

        sel = self.view.sel()
        sel_len = len(sel)

        if not item.appliable_to_selection(sel):
            return error_msg("Numbers of selections mismatched...")

        if sel_len == 1:
            self.view.replace(edit, sel[0], "\n".join(item.texts))
        else:
            for r, texts in zip(sel, repeat_iterable(item.texts, sel_len)):
                self.view.replace(edit, r, texts)

        # make all regions in the selection empty
        pts = [r.b for r in sel]
        sel.clear()
        sel.add_all(pts)

        if promote_pasted_item:
            clipboard.make_texts_latest(item.texts)
