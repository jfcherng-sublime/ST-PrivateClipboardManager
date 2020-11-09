import sublime

from typing import Iterable, List, Set

__all__ = [
    "Clipboard",
    "ClipboardItem",
]


T_SORTING_ORDER = int
T_SELECTION_TEXTS = List[str]


class ClipboardItem:
    _incremental_id = 1

    # consts
    AUTO_ORDER = -1  # type: T_SORTING_ORDER

    def __init__(self, texts: T_SELECTION_TEXTS = [], order: T_SORTING_ORDER = AUTO_ORDER):
        self._id = self.__class__._incremental_id
        self.__class__._incremental_id += 1

        self.texts = texts
        self.order = order  # larger = higher priority

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, self.__class__):
            return False

        return o.texts == self.texts and o.order == self.order

    def __repr__(self) -> str:
        return {
            # ...
            "id": self._id,
            "texts": self.texts,
            "order": self.order,
        }.__repr__()

    def __hash__(self) -> int:
        return (self.texts.__repr__(), self.order).__hash__()

    @property
    def id(self) -> int:
        return self._id

    def appliable_to_selection(self, sel: sublime.Selection) -> bool:
        sel_len = len(sel)
        texts_len = len(self.texts)

        return sel_len == 1 or texts_len == 1 or sel_len == texts_len


class Clipboard:
    # consts
    CAPACITY_UNLIMITED = -1

    def __init__(self, capacity: int = CAPACITY_UNLIMITED) -> None:
        self._items = set()  # type: Set[ClipboardItem]
        self.capacity = capacity

        # cache of the max order in items
        self._max_order = 0  # type: T_SORTING_ORDER

    def __len__(self) -> int:
        return len(self._items)

    def __getitem__(self, idx: int) -> ClipboardItem:
        return self.get_sorted_items()[idx]

    def __iter__(self) -> Iterable[ClipboardItem]:
        return self._items.__iter__()

    def __repr__(self) -> str:
        items = self.get_sorted_items(include_dead=True)
        dead_count = max(0, len(items) - self._capacity)

        return {
            "capacity": self._capacity,
            "capacity_real": self._capacity_real,
            "max_order": self._max_order,
            "items": {
                # ...
                "living": items[-self._capacity :],
                "dead": items[:dead_count],
            },
        }.__repr__()

    @property
    def items(self) -> Set[ClipboardItem]:
        return self._items

    @property
    def capacity(self) -> int:
        return self._capacity

    @capacity.setter
    def capacity(self, value: int) -> None:
        if value > 0:
            self._capacity = value

            # to prevent from deleting an old item everytime when adding a new one
            #
            # for example, if the user set the capacity to 30, the internal capacity is like 61,
            # when the item counts hits 62, do cleanup so that only the latest 30 items are kept
            # by doing so, we delete old items every 30 times
            self._capacity_real = self._capacity * 2 + 1
        else:
            self._capacity = self._capacity_real = value

        assert self._capacity_real >= self._capacity

        self.cleanup()

    def add(self, item: ClipboardItem) -> None:
        if item.order == ClipboardItem.AUTO_ORDER:
            item.order = self.get_next_order()

        self._items.add(item)
        self._suggest_max_order(item.order)

        self.cleanup()

    def add_texts(self, texts: T_SELECTION_TEXTS) -> None:
        # maybe texts already exists?
        success = self.make_texts_latest(texts)

        if not success:
            self.add(ClipboardItem(texts))

        # we don't have to do cleanup here because self.add() will do it
        # and self.make_texts_latest() won't change item counts

    def remove_by_ids(self, ids: Iterable[int]) -> None:
        ids = set(ids)

        self._items -= {item for item in self._items if item.id in ids}

    def make_texts_latest(self, texts: T_SELECTION_TEXTS) -> bool:
        for item in self._items:
            if item.texts == texts:
                if item.order != self._max_order:
                    item.order = self.get_next_order()
                    self._suggest_max_order(item.order)

                return True

        return False

    def get_next_order(self) -> T_SORTING_ORDER:
        return self._max_order + 1

    def get_sorted_items(self, reverse: bool = False, include_dead: bool = False) -> List[ClipboardItem]:
        items = sorted(self._items, key=lambda item: item.order)

        if include_dead:
            if reverse:
                items.reverse()

            return items

        living_items = items[-self._capacity :]

        if reverse:
            living_items.reverse()

        return living_items

    def cleanup(self) -> None:
        if self._capacity > 0 and len(self._items) > self._capacity_real:
            self.remove_by_ids(
                item.id for item in self.get_sorted_items(include_dead=True)[: len(self._items) - self._capacity]
            )

    def clear(self) -> None:
        self.remove_by_ids(item.id for item in self._items)

    def _suggest_max_order(self, order: T_SORTING_ORDER) -> bool:
        if self._max_order < order:
            self._max_order = order

            return True

        return False
