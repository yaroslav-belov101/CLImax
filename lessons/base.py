from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class LessonStep:
    command: str
    description: str  # Описание
    hint: Optional[str] = None  # Подсказка
    strict: bool = False  # Если True — требуется точное совпадение команды


class BaseLesson(ABC):
    @property
    @abstractmethod
    def id(self) -> str:
        pass

    @property
    @abstractmethod
    def title(self) -> str:
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        pass

    @property
    @abstractmethod
    def steps(self) -> List[LessonStep]:
        pass

    def validate_step(self, step_index: int, user_input: str) -> tuple[bool, str]:
        if step_index >= len(self.steps):
            return False, "Шаг не найден"

        step = self.steps[step_index]

        if step.strict:
            is_valid = user_input.strip() == step.command
        else:
            is_valid = user_input.strip().lower() == step.command.lower()

        if is_valid:
            return True, "✓ Верно!"
        else:
            hint = f" (Подсказка: {step.hint})" if step.hint else ""
            return False, f"✗ Неверно.{hint} Ожидалось: {step.command}"

    def get_progress(self, current_step: int) -> tuple[int, int]:
        return (current_step + 1, len(self.steps))
