from rich.console import Console, Group
from rich.panel import Panel
from rich.prompt import Prompt
from rich.text import Text
from rich.live import Live
from rich.align import Align
from rich.progress import (
    Progress,
    SpinnerColumn,
    TextColumn,
    BarColumn,
    TaskProgressColumn,
)
import time
import os
from pyfiglet import Figlet


class CLImaxUI:
    def __init__(self):
        self.console = Console()
        self.center_width = 70

    def clear_screen(self):
        if os.name == "nt":
            os.system("cls")
        else:
            os.system("clear")

    def _get_center_padding(self, content_height: int) -> str:
        terminal_height = self.console.height
        padding = (terminal_height - content_height) // 2
        return "\n" * max(0, padding)

    def show_fullscreen_logo(self):
        self.clear_screen()

        figlet = Figlet(font="big")
        logo_text = figlet.renderText("CLImax")

        content_height = 11
        top_padding = self._get_center_padding(content_height)

        logo_renderable = Align.center(Text(logo_text, style="bold cyan"))

        self.console.print(top_padding, end="")
        self.console.print(logo_renderable)
        self.console.print()

        progress = Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(bar_width=30),
            TaskProgressColumn(),
            console=self.console,
            transient=True,
        )

        task = progress.add_task("[green]Загрузка модулей...", total=100)

        with Live(
            Align.center(progress),
            console=self.console,
            refresh_per_second=20,
            transient=True,
        ) as live:
            for _ in range(100):
                progress.update(task, advance=1)
                time.sleep(0.015)

        self.clear_screen()
        done_text = Panel(
            "[bold green]✓ Загрузка завершена[/bold green]",
            width=self.center_width,
            border_style="green",
        )

        self.console.print(self._get_center_padding(3), end="")
        self.console.print(Align.center(done_text))
        time.sleep(1)
        self.clear_screen()

    def typewrite_centered(self, text: str, speed: float = 0.05):
        displayed = ""

        with Live(console=self.console, refresh_per_second=20) as live:
            for char in text:
                displayed += char
                centered = Align.center(Text(displayed, style="bold cyan"))
                live.update(centered)
                time.sleep(speed)

        self.console.print()

    def show_welcome(self):
        self.show_fullscreen_logo()

        self.typewrite_centered("Добро пожаловать в CLImax", speed=0.05)

        welcome_panel = Panel(
            "[bold cyan]CLImax[/bold cyan] — тренажёр командной строки\n"
            "[dim]Версия 0.1.0[/dim]",
            width=self.center_width,
            border_style="green",
            padding=(1, 4),
        )

        self.console.print(self._get_center_padding(6), end="")
        self.console.print(Align.center(welcome_panel))
        time.sleep(2)
        self.clear_screen()
