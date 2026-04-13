from typing import Optional

from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table
from rich.console import Console
from rich.align import Align

from .base import BaseScreen, ScreenResult, clear_console


class MenuScreen(BaseScreen):
    def __init__(self, console: Console, context: Optional[dict] = None):
        super().__init__(console, context)
        self.options = {
            "1": ("bash", "Bash для начинающих"),
            "2": ("git", "Git основы"),
            "3": ("python", "Python Junior"),
            "0": (None, "Выход"),
        }
        self.center_width = 70

    def on_mount(self) -> None:
        clear_console(self.console)

    def render(self) -> ScreenResult:
        # Создаем контейнер меню
        container = Table.grid(padding=1)
        container.add_column(justify="center", width=self.center_width)

        # Заголовок
        container.add_row(
            Panel.fit(
                "[bold cyan]Главное меню[/bold cyan]", border_style="green", width=50
            )
        )

        # Таблица опций
        table = Table(show_header=False, box=None, width=50)
        table.add_column(style="bold", width=4)
        table.add_column()

        for key, (value, description) in self.options.items():
            style = "red" if key == "0" else "white"
            table.add_row(f"[{key}]", f"[{style}]{description}[/{style}]")

        container.add_row(table)
        container.add_row("")
        container.add_row("[dim]Выберите вариант (0-3)[/dim]")

        centered_content = Align.center(container)

        terminal_height = self.console.height
        content_height = 12  # Приблизительная высота меню
        top_padding = (terminal_height - content_height) // 2

        self.console.print("\n" * max(0, top_padding), end="")
        self.console.print(centered_content)

        left_padding = " " * ((self.console.width - 20) // 2)
        choice = Prompt.ask(f"{left_padding}>>", choices=list(self.options.keys()))

        selected_value = self.options[choice][0]

        if selected_value is None:
            return ScreenResult.exit()

        return ScreenResult.goto("lesson", track=selected_value)

    def on_unmount(self) -> None:
        pass
