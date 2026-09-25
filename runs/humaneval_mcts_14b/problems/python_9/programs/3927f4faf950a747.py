from typing import List

def rolling_max(numbers: List[int]) -> List[int]:
    if not numbers:
        return []
    
    rolling_max_values = []
    current_max = numbers[0]
    
    for number in numbers:
        if number > current_max:
            current_max = number
        rolling_max_values.append(current_max)
    
    return rolling_max_values

# Example usage
if __name__ == "__main__":
    print(rolling_max([1, 2, 3, 2, 3, 4, 2]))  # Output: [1, 2, 3, 3, 3, 4, 4]