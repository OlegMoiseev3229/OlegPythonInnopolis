import random as rnd


class Human:
    genome_count = 46

    def __init__(self, name: str, age: int, bio: str = ""):
        self.name = name
        self.age = age
        self.bio = bio

    def tell_about(self):
        print(f"Hi, I'm {self.name}, I'm {self.age} years old. \n{self.bio}")


class Student:

    def __init__(self, name: str, age: int, grades: list):
        self.name = name
        self.age = age
        self.grades = grades

    def calculate_scholarship(self) -> float:
        if len(self.grades) == 0:
            raise ZeroDivisionError(f"Student {self.name} has no grades")
        return sum(self.grades)/len(self.grades) * 100

    def add_grade(self, grade):
        self.grades.append(grade)

    def clear_grades(self):
        self.grades.clear()

    def __repr__(self):
        return f"{self.__class__.__name__}(name='{self.name}', age={self.age}, grades={self.grades=})"


def main():
    oleg = Student("Oleg", 17, [])
    oleg.add_grade(5)
    print(oleg)


if __name__ == '__main__':
    main()

