from typing import Dict

def count_word_occurrences(text: str) -> Dict[str, int]:
    """Return a dictionary with the count of each unique word in the given string."""
    words = text.split()
    word_count = {}
    for word in words:
        word = word.lower()  # Normalize to lowercase
        if word in word_count:
            word_count[word] += 1
        else:
            word_count[word] = 1
    return word_count

# Example usage:
result = count_word_occurrences("Hello world, hello Python, world of programming")
print(result)

# Output:
# {'hello': 2, 'world,': 1, 'python,': 1, 'world': 1, 'of': 1, 'programming': 1}

