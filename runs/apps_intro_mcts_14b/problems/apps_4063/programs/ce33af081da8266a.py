import sys
from collections import Counter

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    difficulties = list(map(int, data[1:]))
    
    # Sort the difficulties
    difficulties.sort()
    
    # Calculate the target number of problems for each category
    target = N // 2
    
    # Initialize the count of valid K values
    valid_K_count = 0
    
    # Use a set to track unique difficulties
    unique_difficulties = set(difficulties)
    
    # Iterate through each unique difficulty
    for K in unique_difficulties:
        # Count the number of problems with difficulty >= K
        count_ARC = sum(1 for d in difficulties if d >= K)
        
        # Check if the count matches the target
        if count_ARC == target:
            valid_K_count += 1
    
    # Print the result
    print(valid_K_count)

if __name__ == "__main__":
    main()