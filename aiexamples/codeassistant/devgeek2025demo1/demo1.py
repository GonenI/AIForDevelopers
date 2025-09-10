class Student:
    def __init__(self, name, age, student_id):
        """
        Constructor for Student class
        
        Args:
            name (str): Student's name
            age (int): Student's age
            student_id (str/int): Student's ID
        """
        self.name = name
        self.age = age
        self.id = student_id
    
    def get_name(self):
        """
        Get the student's name
        
        Returns:
            str: Student's name
        """
        return self.name
    
    def get_age(self):
        """
        Get the student's age
        
        Returns:
            int: Student's age
        """
        return self.age
    
    def get_id(self):
        """
        Get the student's ID
        
        Returns:
            str/int: Student's ID
        """
        return self.id
    
    def __str__(self):
        """
        String representation of the Student object
        
        Returns:
            str: Formatted string with student information
        """
        return f"Student(Name: {self.name}, Age: {self.age}, ID: {self.id})"

# Example usage
if __name__ == "__main__":
    # Create a student instance
    student1 = Student("Alice Johnson", 20, "S12345")
    
    # Use the getters
    print(f"Name: {student1.get_name()}")
    print(f"Age: {student1.get_age()}")
    print(f"ID: {student1.get_id()}")
    
    # Use the string representation
    print(student1)