def bubble_sort(arr):
    n = len(arr)
    # Traverse through all array elements
    for i in range(n):
        # Flag to optimize the algorithm
        swapped = False
        
        # Last i elements are already in place
        for j in range(0, n-i-1):
            # Compare adjacent elements
            if arr[j] > arr[j+1]:
                # Swap if the element found is greater than the next element
                arr[j], arr[j+1] = arr[j+1], arr[j]
                swapped = True
        
        # If no swapping occurred in this pass, array is already sorted
        if not swapped:
            break
    
    return arr

if __name__ == "__main__":
    # Create a list with random numbers
    numbers = [64, 34, 25, 12, 22, 11, 90]
    
    print("Original array:", numbers)
    
    # Sort the array using bubble sort
    sorted_numbers = bubble_sort(numbers)
    
    print("Sorted array:", sorted_numbers) 