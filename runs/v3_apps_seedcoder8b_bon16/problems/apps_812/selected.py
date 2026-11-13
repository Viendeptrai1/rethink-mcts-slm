def find_arithmetic_index(n, b):
    if n == 2:
        return 1

    # Try to find an arithmetic progression by removing each element
    for j in range(n):
        # Create a new sequence excluding the j-th element
        remaining = b[:j] + b[j+1:]
        
        # Sort the remaining sequence
        remaining.sort()
        
        # Check if the sorted sequence forms an arithmetic progression
        if is_arithmetic_progression(remaining):
            return j + 1
    
    return -1

def is_arithmetic_progression(seq):
    if len(seq) <= 2:
        return True

    # Calculate the difference of the first two elements
    diff = seq[1] - seq[0]
    
    # Check if each consecutive pair of elements has the same difference
    for i in range(2, len(seq)):
        if seq[i] - seq[i - 1] != diff:
            return False
    
    return True

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    b = list(map(int, data[1:n+1]))
    
    result = find_arithmetic_index(n, b)
    print(result)