from .base import BaseLesson, LessonStep


class BashBeginnerLesson(BaseLesson):
    @property
    def id(self) -> str:
        return "bash"

    @property
    def title(self) -> str:
        return "Bash для начинающих"

    @property
    def description(self) -> str:
        return "Основы навигации в терминале Linux/Mac"

    @property
    def steps(self) -> list[LessonStep]:
        return [
            LessonStep(
                command="pwd",
                description="Узнайте, в какой директории вы сейчас находитесь",
                hint="Print Working Directory",
            ),
            LessonStep(
                command="ls",
                description="Посмотрите содержимое текущей папки",
                hint="LiSt",
            ),
            LessonStep(
                command="ls -la",
                description="Покажите все файлы, включая скрытые, с подробностями",
                hint="Добавьте флаги -la к команде ls",
            ),
            LessonStep(
                command="cd ~",
                description="Перейдите в домашнюю директорию",
                hint="Change Directory ~ (тильда = дом)",
            ),
            LessonStep(
                command="clear",
                description="Очистите экран терминала",
                hint="Или Ctrl+L",
            ),
        ]
