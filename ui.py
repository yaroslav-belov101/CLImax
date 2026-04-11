from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.text import Text
from rich.live import Live
from rich.align import Align
from rich.progress import Progress
import time
import os
from pyfiglet import Figlet


class CLImaxUI:
    def __init__(self):
        self.console = Console()

    def clear_screen(self):
        if os.name == "nt":
            os.system("cls")
        else:
            os.system("clear")

    def show_fullscreen_logo(self):
        self.clear_screen()

        figlet = Figlet(font="big")
        logo_text = figlet.renderText("CLImax")

        height = self.console.height
        top_padding = "\n" * (height // 3)

        self.console.print(top_padding, end="")
        self.console.print(Align.center(logo_text), style="bold cyan")

        with Progress(
            console=self.console, transient=True, refresh_per_second=10
        ) as progress:
            task = progress.add_task("[green]Загрузка модулей...", total=100)

            for _ in range(100):
                progress.update(task, advance=1)
                time.sleep(0.02)

        self.clear_screen()
        self.console.print(top_padding, end="")
        self.console.print(Align.center("[bold green]Пошел нахуй ✓ [/bold green]"))
        time.sleep(1)
        self.clear_screen()

    def typewrite(self, text: str, speed: float = 0.05):
        displayed = ""
        with Live(console=self.console, refresh_per_second=20) as live:
            for char in text:
                displayed += char
                rich_text = Text(displayed, style="bold cyan")
                live.update(rich_text)
                time.sleep(speed)

            self.console.print()

    def show_welcome(self):
        self.show_fullscreen_logo()
        self.typewrite("Добро пожаловать в CLImax", speed=0.05)
        self.console.print(
            Panel.fit(
                "[bold cyan]CLImax[/bold cyan] — тренажёр командной строки\n"
                "[dim]Версия 0.0.1[/dim]",
                border_style="green",
            )
        )
