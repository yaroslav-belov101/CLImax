from .base import BaseLesson, LessonStep


class GitBasicsLesson(BaseLesson):
    @property
    def id(self) -> str:
        return "git"

    @property
    def title(self) -> str:
        return "Git основы"

    @property
    def description(self) -> str:
        return "Базовые команды системы контроля версий"

    @property
    def steps(self) -> list[LessonStep]:
        return [
            LessonStep(
                command="git init",
                description="Инициализируйте новый Git-репозиторий в текущей папке",
                hint="Инициализация",
            ),
            LessonStep(
                command="git status",
                description="Проверьте статус файлов в репозитории",
                hint="Статус",
            ),
            LessonStep(
                command="git add .",
                description="Добавьте все измененные файлы в индекс (staging area)",
                hint="Точка означает 'все файлы'",
            ),
            LessonStep(
                command='git commit -m "first commit"',
                description="Создайте первый коммит с сообщением",
                hint="Не забудьте кавычки вокруг сообщения",
                strict=True,
            ),
            LessonStep(
                command="git log",
                description="Посмотрите историю коммитов",
                hint="Журнал",
            ),
        ]
