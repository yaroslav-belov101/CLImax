from abc import ABC, abstractmethod
from rich.console import Console
from typing import Optional, final
from dataclasses import dataclass

from rich.align import Align
from rich.layout import Layout


@dataclass(frozen=True)
class ScreenResult:
    next_screen: Optional[str]
    data: Optional[dict] = None

    @classmethod
    def exit(cls) -> "ScreenResult":
        return cls(next_screen=None)

    @classmethod
    def goto(cls, screen_name: str, **kwargs) -> "ScreenResult":
        return cls(next_screen=screen_name, data=kwargs)


class BaseScreen(ABC):
    def __init__(self, console: Console, context: Optional[dict] = None):
        self._console = console
        self._context = context or {}
        self._mounted = False

    def render_centered(self, content, max_width: int = 80):
        width = min(max_width, self.console.width - 4)
        width = max(width, 40)

        layout = Layout()
        layout.split_row(
            Layout(name="left"),
            Layout(content, name="center", size=width),
            Layout(name="right"),
        )

        return Align.center(layout)

    def clear_and_center(self, content, max_width: int = 80):
        clear_console(self.console)
        self.console.print(self.render_centered(content, max_width))

    @property
    def console(self) -> Console:
        return self._console

    @property
    def context(self) -> dict:
        return self._context

    @final
    def mount(self) -> None:
        if self._mounted:
            raise RuntimeError(f"{self.__class__.__name__} уже смонтирован")

        self.on_mount()
        self._mounted = True

    @abstractmethod
    def on_mount(self) -> None:
        pass

    @abstractmethod
    def render(self) -> ScreenResult:
        pass

    @final
    def unmount(self) -> None:
        if not self._mounted:
            return

        self.on_unmount()
        self._mounted = False

    @abstractmethod
    def on_unmount(self) -> None:
        pass

    def __enter__(self):
        self.mount()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.unmount()
        return False


class ScreenError(Exception):
    pass


def clear_console(console: Console) -> None:
    import os

    try:
        if os.name == "nt":
            os.system("cls")
        else:
            os.system("clear")
    except Exception:
        console.print("\n" * 50)
