from typing import List

def mean_absolute_deviation(numbers: List[float]) -> float:
    if not numbers:
        raise ValueError("The list of numbers cannot be empty")
    
    mean = sum(numbers) / len(numbers)
    mad = sum(abs(x - mean) for x in numbers) / len(numbers)
    return mad

# Example usage
if __name__ == "__main__":
    print(mean_absolute_deviation([1.0, 2.0, 3.0, 4.0]))  # Output: 1.0