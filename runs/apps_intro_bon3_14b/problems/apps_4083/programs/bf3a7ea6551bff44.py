import sys
from collections import Counter

def min_operations_to_equal_numbers(n, k, a):
    # Count the frequency of each number in the array
    count = Counter(a)
    
    # Sort the frequencies in descending order
    freqs = sorted(count.values(), reverse=True)
    
    # Calculate the minimum number of operations needed
    operations = 0
    for i in range(k):
        if i < len(freqs):
            operations += n - freqs[i]
        else:
            operations += n
    
    return operations

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    k = int(data[1])
    a = list(map(int, data[2:]))
    
    result = min_operations_to_equal_numbers(n, k, a)
    print(result)

if __name__ == "__main__":
    main()