import sys
from pathlib import Path
from typing import Optional, Type, Dict

sys.path.insert(0, str(Path(__file__).parent))

from rich.console import Console
from rich.panel import Panel

from UI.ui import CLImaxUI
from UI.screens.base import BaseScreen, ScreenResult, ScreenError
from UI.screens.menu import MenuScreen
from UI.screens.lesson import LessonScreen


class ScreenManager:
    def __init__(self, console: Console):
        self.console = console
        self.screens: Dict[str, Type[BaseScreen]] = {
            "menu": MenuScreen,
            "lesson": LessonScreen,
        }
        self.context: dict = {}

    def get_screen(self, name: str) -> Optional[BaseScreen]:
        if name not in self.screens:
            self.console.print(f"[red]Ошибка: экран '{name}' не найден[/]")
            return None

        screen_class = self.screens[name]
        return screen_class(self.console, self.context)

    def run(self, start_screen: str = "menu"):
        current_name = start_screen
        while current_name:
            screen = self.get_screen(current_name)
            if screen is None:
                self.console.print("[red]Не могу показать экран. Выход.[/]")
                break
            try:
                with screen:
                    result = screen.render()

                if result.next_screen is None:
                    break

                current_name = result.next_screen

                if result.data:
                    self.context.update(result.data)

            except ScreenError as e:
                self.console.print(f"[red]Ошибка экрана: {e}[/]")
                break
            except KeyboardInterrupt:
                self.console.print("\n[dim]Прервано пользователем[/]")
                break
            except Exception as e:
                self.console.print(f"[red]Неожиданная ошибка: {e}[/]")
                import traceback

                self.console.print(traceback.format_exc())
                break

        self.console.print(Panel("[bold green]До свидания![/]", border_style="green"))


def main():
    ui = CLImaxUI()
    ui.show_welcome()

    console = ui.console
    manager = ScreenManager(console)
    manager.run(start_screen="menu")


if __name__ == "__main__":
    main()
