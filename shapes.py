TAU = 6.2831853071795864769252867665


class Shape:
    def __init__(self):
        pass

    def calculate_area(self):
        pass


class Rectangle(Shape):
    def __init__(self, a, b):
        self._width = a
        self._height = b
        super().__init__()

    def calculate_area(self):
        return self._width * self._height

    def size(self):
        return self._width, self._height

    def width(self):
        return self._width

    def height(self):
        return self._height


class Square(Rectangle):
    def __init__(self, side):
        super().__init__(side, side)

    def side_length(self):
        return self._width


class Circle(Shape):
    def __init__(self, r):
        self._radius = r
        super(Circle, self).__init__()

    def calculate_area(self):
        return self._radius * self._radius * TAU/2

    def radius(self):
        return self._radius
