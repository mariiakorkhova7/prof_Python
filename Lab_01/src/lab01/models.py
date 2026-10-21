from dataclasses import dataclass

@dataclass
class Student:
    full_name: str
    subject: str
    grades: list[float]
    
    @property
    def average_grade(self) -> float:
        return sum(self.grades) / len(self.grades) if self.grades else 0.0