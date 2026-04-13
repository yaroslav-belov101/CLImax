from .base import BaseLesson, LessonStep


class PythonJuniorLesson(BaseLesson):
    @property
    def id(self) -> str:
        return "python"

    @property
    def title(self) -> str:
        return "Python Junior"

    @property
    def description(self) -> str:
        return "Базовые команды Python в CLI"

    @property
    def steps(self) -> list[LessonStep]:
        return [
            LessonStep(
                command="python --version",
                description="Проверьте установленную версию Python",
                hint="или python3 --version",
            ),
            LessonStep(
                command="python -c \"print('Hello World')\"",
                description="Выполните Python-код прямо в командной строке",
                hint="Флаг -c позволяет передать код строкой",
                strict=True,
            ),
            LessonStep(
                command="pip list",
                description="Покажите список установленных пакетов",
                hint="Package Installer for Python",
            ),
            LessonStep(
                command="python -m venv venv",
                description="Создайте виртуальное окружение с именем 'venv'",
                hint="Модуль venv",
            ),
        ]
