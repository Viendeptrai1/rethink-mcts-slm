def max_consecutive_erasable_elements(n, array):
    max_erase = 0
    for start in range(n):
        for end in range(start + 1, n):
            # Remaining array after erasing elements from start to end - 1
            remaining = array[:start] + array[end:]
            # Check if the remaining array is still a valid increasing sequence
            if all(remaining[i] < remaining[i + 1] for i in range(len(remaining) - 1)):
                max_erase = max(max_erase, end - start)
    return max_erase

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    array = list(map(int, data[1:n+1]))
    
    result = max_consecutive_erasable_elements(n, array)
    print(result)