from abc import ABC, abstractmethod
import math


class Shape(ABC):
    """Abstract base class for all shapes"""
    
    def __init__(self, name):
        self.name = name
    
    @abstractmethod
    def area(self):
        """Calculate the area of the shape"""
        pass
    
    @abstractmethod
    def perimeter(self):
        """Calculate the perimeter of the shape"""
        pass
    
    def __str__(self):
        return f"{self.name} - Area: {self.area():.2f}, Perimeter: {self.perimeter():.2f}"


class Rect
    """Rectangle class that inherits from Shape"""
    
    def __init__(self, width, height):
        super().__init__("Rectangle")
        self.width = width
        self.height = height
    
    def area(self):
        """Calculate rectangle area: width * height"""
        return self.width * self.height
    
    def perimeter(self):
        """Calculate rectangle perimeter: 2 * (width + height)"""
        return 2 * (self.width + self.height)


class Circle
    """Circle class that inherits from Shape"""
    
    def __init__(self, radius):
        super().__init__("Circle")
        self.radius = radius
    
    def area(self):
        """Calculate circle area: π * r²"""
        return math.pi * self.radius ** 2
    
    def perimeter(self):
        """Calculate circle perimeter (circumference): 2 * π * r"""
        return 2 * math.pi * self.radius


# Example usage and testing
if __name__ == "__main__":
    # Create instances
    rectangle = Rect(5, 3)
    circle = Circle(4)
    
    # Print information about each shape
    print(rectangle)
    print(circle)
    
    # Test individual methods
    print(f"\nRectangle details:")
    print(f"Width: {rectangle.width}, Height: {rectangle.height}")
    print(f"Area: {rectangle.area()}")
    print(f"Perimeter: {rectangle.perimeter()}")
    
    print(f"\nCircle details:")
    print(f"Radius: {circle.radius}")
    print(f"Area: {circle.area():.2f}")
    print(f"Perimeter: {circle.perimeter():.2f}")
