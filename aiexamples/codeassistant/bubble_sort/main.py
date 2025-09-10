from create_number_list import create_number_list
from bubble_sort import bubble_sort

def main():
    """Main function to create, sort, and display the list."""
    numbers = create_number_list()
    print("Original list:", numbers)
    sorted_numbers = bubble_sort(numbers)
    print("Sorted list:", sorted_numbers)

if __name__ == "__main__":
    main()