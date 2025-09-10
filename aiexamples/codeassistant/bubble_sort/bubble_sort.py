def bubble_sort(numbers):
    """Sorts a list of numbers using the bubble sort algorithm."""
    n = len(numbers)
    for i in range(n):
        # Last i elements are already sorted
        for j in range(0, n - i - 1):
            if numbers[j] > numbers[j + 1]:
                # Swap if the element found is greater than the next element
                numbers[j], numbers[j + 1] = numbers[j + 1], numbers[j]
    return numbers