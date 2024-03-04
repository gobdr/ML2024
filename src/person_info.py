from enum import Enum


class Gender(Enum):
    MALE = "male"
    FEMALE = "female"

from enum import Enum

class ActivityLevel(Enum):
    NO = "no",
    MINIMAL = "minimal"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "veryhigh"

class Goal(Enum):
    SLIGHT_GAIN = "slightgain"
    MODERATE_GAIN = "moderategain"
    EXTREME_GAIN = "extremegain"
    MAINTENANCE = "weightmaintenance"
    SLIGHT_LOSS = "slightloss"
    MODERATE_LOSS = "moderateloss"
    EXTREME_LOSS = "extremeloss"


class PersonInfo:
    def __init__(self, age: int, gender: Gender, height: int, weight: int, activity_level: ActivityLevel, goal: Goal):
        self.age = age
        self.gender = gender
        self.height = height
        self.weight = weight
        self.activity_level = activity_level
        self.goal = goal

    def __str__(self):
        return (f"+----------ИНФОРМАЦИЯ О ЧЕЛОВЕКЕ----------+\n"
                f"Возраст: {self.age}\n"
                f"Пол: {self.gender}\n"
                f"Рост: {self.height}\n"
                f"Вес: {self.weight}\n"
                f"Уровень активности: {self.activity_level}\n"
                f"Цель: {self.goal}\n"
                f"+-------------------------------+\n")
