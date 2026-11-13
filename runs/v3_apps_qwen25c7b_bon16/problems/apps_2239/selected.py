def min_rolls_to_score(target):
    # Since the dice has faces with values 2, 3, 4, 5, 6, 7
    # We need to find the minimum number of rolls to achieve the target score
    # This is equivalent to finding the minimum number of terms whose sum is target
    # where each term is between 2 and 7

    # We start with the smallest possible number of rolls (target / 2 since 2 is the smallest face)
    min_rolls = target // 2
    
    # Iterate to ensure we find the exact minimum
    while True:
        current_sum = min_rolls * 2
        remainder = target - current_sum
        
        # Check if the remainder can be formed using the faces {3, 4, 5, 6, 7}
        if remainder >= 0 and remainder <= min_rolls * 5:
            return min_rolls
        
        min_rolls += 1

# Read input
import sys
input = sys.stdin.read
data = input().split()

t = int(data[0])
queries = list(map(int, data[1:]))

# Process each query
results = [min_rolls_to_score(x) for x in queries]

# Output results
print("\n".join(map(str, results)))