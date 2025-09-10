
# writer: Gonen, time: 11:32 AM
from interfaces.iperson import IPerson

class Person(IPerson):
    def __init__(self, name: str, age: int) -> None:
        self._name: str = name
        self._age: int = age

    @staticmethod
    def getName(obj: 'Person') -> str:
        return obj._name

    @staticmethod
    def getAge(obj: 'Person') -> int:
        return obj._age