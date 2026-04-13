from typing import Dict, Type, Optional
from .base import BaseLesson

from .bash_beginner import BashBeginnerLesson
from .git_basics import GitBasicsLesson
from .python_junior import PythonJuniorLesson


class LessonRegistry:
    def __init__(self):
        self._lessons: Dict[str, BaseLesson] = {}
        self._register_default_lessons()

    def _register_default_lessons(self):
        lessons = [
            BashBeginnerLesson(),
            GitBasicsLesson(),
            PythonJuniorLesson(),
        ]
        for lesson in lessons:
            self.register(lesson)

    def register(self, lesson: BaseLesson) -> None:
        self._lessons[lesson.id] = lesson

    def get(self, lesson_id: str) -> Optional[BaseLesson]:
        return self._lessons.get(lesson_id)

    def list_all(self) -> Dict[str, BaseLesson]:
        return self._lessons.copy()

    def get_menu_items(self) -> Dict[str, tuple[str, str]]:
        return {
            lid: (lesson.title, lesson.description)
            for lid, lesson in self._lessons.items()
        }


_registry = LessonRegistry()


def get_lesson(lesson_id: str) -> Optional[BaseLesson]:
    return _registry.get(lesson_id)


def register_lesson(lesson: BaseLesson) -> None:
    _registry.register(lesson)


def get_available_lessons() -> Dict[str, BaseLesson]:
    return _registry.list_all()


def get_lesson_menu() -> Dict[str, tuple[str, str]]:
    return _registry.get_menu_items()


__all__ = [
    "BaseLesson",
    "LessonStep",
    "get_lesson",
    "register_lesson",
    "get_available_lessons",
    "get_lesson_menu",
]
