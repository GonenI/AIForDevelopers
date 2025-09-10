from abc import ABC, abstractmethod
from typing import Any

class IStudent(ABC):
    @staticmethod
    @abstractmethod
    def getStudentId(obj: Any) -> str:
        pass
