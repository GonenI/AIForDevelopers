from abc import ABC, abstractmethod
from typing import Any

class IPerson(ABC):
    @staticmethod
    @abstractmethod
    def getName(obj: Any) -> str:
        pass

    @staticmethod
    @abstractmethod
    def getAge(obj: Any) -> int:
        pass
