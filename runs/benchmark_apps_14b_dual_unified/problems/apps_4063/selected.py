import sys
from collections import Counter

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    difficulties = list(map(int, data[1:]))
    
    # Count the frequency of each difficulty level
    freq = Counter(difficulties)
    
    # Sort the unique difficulties
    unique_difficulties = sorted(freq.keys())
    
    # Calculate the prefix sum of frequencies
    prefix_sum = [0] * (len(unique_difficulties) + 1)
    for i in range(len(unique_difficulties)):
        prefix_sum[i + 1] = prefix_sum[i] + freq[unique_difficulties[i]]
    
    # Find the number of valid K values
    count = 0
    target = N // 2
    for i in range(len(unique_difficulties)):
        if prefix_sum[-1] - prefix_sum[i + 1] == target:
            count += 1
    
    print(count)

if __name__ == "__main__":
    main()