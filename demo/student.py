from interfaces.istudent import IStudent
from person import Person

class Student(Person, IStudent):
    def __init__(self, name: str, age: int, studentId: str) -> None:
        super().__init__(name, age)
        self._studentId: str = studentId

    @staticmethod
    def getStudentId(obj: 'Student') -> str:
        return obj._studentId
