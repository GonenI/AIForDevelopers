from utils import print_separator, format_title, MAX_FIBONACCI_NUMBERS

def next_fibonacci():
    """
    Generator function that yields the next Fibonacci number in the sequence.
    First two numbers are 0 and 1, each subsequent number is the sum of the previous two.
    """
    # Initialize the first two numbers
    a, b = 0, 1
    
    while True:
        # Yield current number
        yield a
        # Calculate next number and update values
        a, b = b, a + b

# Example usage:
if __name__ == "__main__":
    # Create fibonacci generator and print numbers
    fib = next_fibonacci()
    print(format_title("Fibonacci Numbers"))
    for _ in range(MAX_FIBONACCI_NUMBERS):
        print(next(fib), end=" ")
    
    print_separator()
    
    # Get and print cat fact
    from cat_fact import get_cat_fact
    fact = get_cat_fact()
    if fact:
        print(format_title("Cat Fact of the Day"))
        print(fact)