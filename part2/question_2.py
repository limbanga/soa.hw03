from typing import List, Union

def filter_even_numbers(numbers: List[Union[int, float]]) -> List[int]:
    """Return a list of even integers from the given list of integers or floats."""
    return [int(num) for num in numbers if isinstance(num, (int, float)) and int(num) % 2 == 0]

# Example usage:
result = filter_even_numbers([5, 10.2, 15, 20, 25.5, 30])
print(result)  # Output: [10, 20, 30]

result = filter_even_numbers([5, 10.2, 15, 20, 25.5, 30, '40'])
print(result)  # Output: [10, 20, 30]

