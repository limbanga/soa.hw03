def add_numbers(num1: float, num2: float) -> float:
    return num1 + num2

# Example usage:
result_int = add_numbers(5, 10)  # Both are integers
result_float = add_numbers(5.5, 10.2)  # Both are floats
result_mixed = add_numbers(5, 10.2)  # One is an integer, the other is a float

print(result_int)    # Output: 15
print(result_float)  # Output: 15.7
print(result_mixed)  # Output: 15.2