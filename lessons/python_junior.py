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
        return "Базовые команды Python"

    @property
    def steps(self) -> list[LessonStep]:
        return [
            LessonStep(
                command="print",
                description="Выводит на экран содержимое",
                hint="print('Hellow world')",
            ),
            LessonStep(
                command="input()",
                description="Создание переменных",
                hint="a = input()",
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
