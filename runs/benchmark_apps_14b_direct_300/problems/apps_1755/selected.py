import sys

def min_operations_to_increasing(n, k, a, b):
    if k == 0:
        # If no indices are fixed, we can change all elements to make the array increasing
        return n - 1
    
    # Convert b to a set for O(1) lookups
    b_set = set(b)
    
    # Initialize the result with the number of fixed indices
    result = k
    
    # Iterate through the array and count the number of changes needed
    for i in range(1, n):
        if i + 1 not in b_set and a[i] >= a[i - 1]:
            # We need to change a[i] to be greater than a[i-1]
            result += 1
    
    return result

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    index = 0
    n = int(data[index])
    k = int(data[index + 1])
    index += 2
    
    a = list(map(int, data[index:index + n]))
    index += n
    
    if k > 0:
        b = list(map(int, data[index:index + k]))
    else:
        b = []
    
    result = min_operations_to_increasing(n, k, a, b)
    print(result)

if __name__ == "__main__":
    main()