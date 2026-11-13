def max_consecutive_elements_to_erase(n, array):
    max_erase = 0
    for i in range(n):
        for j in range(i, n):
            # Create a new array excluding the elements from i to j
            new_array = array[:i] + array[j+1:]
            if can_restore(new_array):
                max_erase = max(max_erase, j - i + 1)
    return max_erase

def can_restore(array):
    if not array:
        return True
    n = len(array)
    # Check if the array can be restored by checking the differences
    for i in range(1, n):
        if array[i] - array[i-1] > 1:
            return False
    return True

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    array = list(map(int, data[1:n+1]))
    
    result = max_consecutive_elements_to_erase(n, array)
    print(result)

if __name__ == "__main__":
    main()