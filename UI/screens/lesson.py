from typing import Optional
from rich.panel import Panel
from rich.prompt import Prompt
from rich.console import Console
from rich.align import Align
from rich.table import Table
from rich.text import Text

from .base import BaseScreen, ScreenResult, clear_console
from lessons import get_lesson, BaseLesson


class LessonScreen(BaseScreen):
    def __init__(self, console: Console, context: Optional[dict] = None):
        super().__init__(console, context)
        self.track_id = self.context.get("track", "unknown")
        self.lesson: Optional[BaseLesson] = get_lesson(self.track_id)
        self.current_step = 0
        self.center_width = 70

    def on_mount(self) -> None:
        clear_console(self.console)
        if self.lesson:
            self.current_step = 0

    def _center_padding(self, height: int = 10) -> str:
        # Возвращает строку с отступами
        pad = (self.console.height - height) // 2
        return "\n" * max(0, pad)

    def _centered_input(self, prompt_text: str = ">>") -> str:
        # Выводит prompt и возвращает ввод пользователя
        left_padding = (self.console.width - len(prompt_text) - 2) // 2
        spaces = " " * max(0, left_padding)

        # Выводим prompt
        self.console.print(f"{spaces}[bold cyan]{prompt_text}[/bold cyan] ", end="")

        # Читаем ввод
        return input()

    def render(self) -> ScreenResult:
        if not self.lesson:
            return self._show_error()

        # Вертикальный отступ
        self.console.print(self._center_padding(14), end="")

        # Заголовок урока
        header = Panel(
            f"[bold cyan]{self.lesson.title}[/bold cyan]\n[dim]{self.lesson.description}[/dim]",
            width=self.center_width,
            border_style="blue",
        )
        self.console.print(Align.center(header))
        self.console.print()

        # Прогресс
        current, total = self.lesson.get_progress(self.current_step)
        progress_bar = "█" * current + "░" * (total - current)
        self.console.print(
            Align.center(f"[cyan]{progress_bar}[/cyan] [dim]{current}/{total}[/dim]")
        )
        self.console.print()

        if self.current_step >= len(self.lesson.steps):
            return self._show_completion()

        # Текущий шаг
        step = self.lesson.steps[self.current_step]

        step_panel = Panel(
            f"[bold]Задание:[/bold] {step.description}\n\n"
            f"[dim]Ожидается: [green]{step.command}[/green][/dim]",
            width=self.center_width - 10,
            border_style="yellow",
            padding=(1, 2),
        )
        self.console.print(Align.center(step_panel))
        self.console.print()

        # Меню действий
        actions = Table.grid(padding=1)
        actions.add_column(justify="center")
        actions.add_row("[dim][enter] — выполнить команду[/dim]")
        actions.add_row("[dim][hint] — подсказка[/dim]")
        actions.add_row("[dim][skip] — пропустить[/dim]")
        actions.add_row("[dim][menu] — выход в меню[/dim]")

        self.console.print(Align.center(actions))
        self.console.print()

        # Ввод действия
        self.console.print(Align.center("[dim]Выберите действие и нажмите Enter[/dim]"))
        action = self._centered_input(">>")

        # Валидация ввода
        valid_choices = ["enter", "skip", "menu", "hint", ""]
        if action not in valid_choices:
            action = "enter"

        if action == "menu":
            return ScreenResult.goto("menu")

        elif action == "hint" and step.hint:
            hint_panel = Panel(
                f"💡 {step.hint}", width=self.center_width - 20, border_style="yellow"
            )
            self.console.print(Align.center(hint_panel))
            self.console.print(Align.center("[dim]Нажмите Enter...[/dim]"))
            input()
            return self.render()

        elif action == "skip":
            self.current_step += 1
            return self.render()

        elif action == "enter" or action == "":
            self.console.print(
                Align.center("[bold green]$[/bold green] Введите команду:")
            )
            user_cmd = self._centered_input("$")

            is_valid, message = self.lesson.validate_step(self.current_step, user_cmd)

            msg_color = "green" if is_valid else "red"
            self.console.print(Align.center(f"[{msg_color}]{message}[/{msg_color}]"))

            if is_valid:
                self.current_step += 1
                if self.current_step < len(self.lesson.steps):
                    self.console.print(
                        Align.center("[dim]Нажмите Enter для продолжения...[/dim]")
                    )
                    input()
            else:
                self.console.print(
                    Align.center("[dim]Нажмите Enter чтобы повторить...[/dim]")
                )
                input()

            return self.render()

        return self.render()

    def _show_completion(self) -> ScreenResult:
        completion = Panel(
            "[bold green]🎉 Поздравляем![/bold green]\n\n"
            f"Вы завершили урок:\n[cyan]{self.lesson.title}[/cyan]",
            width=self.center_width,
            border_style="green",
            padding=(1, 2),
        )

        self.console.print(Align.center(completion))
        self.console.print()

        choices = Table.grid(padding=1)
        choices.add_column(justify="center")
        choices.add_row("[1] В главное меню")
        choices.add_row("[2] Пройти снова")
        choices.add_row("[0] Выход")

        self.console.print(Align.center(choices))
        self.console.print()

        self.console.print(Align.center("[dim]Выберите вариант (0-2)[/dim]"))
        action = self._centered_input(">>")

        if action == "0":
            return ScreenResult.exit()
        elif action == "2":
            self.current_step = 0
            return self.render()
        else:
            return ScreenResult.goto("menu")

    def _show_error(self) -> ScreenResult:
        error = Panel(
            f"[red]Ошибка: урок '{self.track_id}' не найден[/red]",
            width=self.center_width,
            border_style="red",
        )
        self.console.print(self._center_padding(5), end="")
        self.console.print(Align.center(error))
        self.console.print(Align.center("[dim]Нажмите Enter...[/dim]"))
        input()
        return ScreenResult.goto("menu")

    def on_unmount(self) -> None:
        pass
