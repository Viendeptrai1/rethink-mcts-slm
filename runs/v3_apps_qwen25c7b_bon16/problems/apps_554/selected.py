def max_happiness(n, m, a, subarrays):
    # Create a list to keep track of the contribution of each flower
    contributions = [0] * n
    
    # Iterate over each subarray
    for start, end in subarrays:
        # Increment the contribution for each flower in the current subarray
        for i in range(start - 1, end):
            contributions[i] += 1
    
    # Calculate the total happiness by summing up the contributions of all flowers
    total_happiness = sum(mood * count for mood, count in zip(a, contributions))
    
    return total_happiness

# Example usage:
if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    m = int(data[1])
    a = list(map(int, data[2:2+n]))
    subarrays = []
    
    index = 2 + n
    for _ in range(m):
        start = int(data[index])
        end = int(data[index+1])
        subarrays.append((start, end))
        index += 2
    
    result = max_happiness(n, m, a, subarrays)
    print(result)