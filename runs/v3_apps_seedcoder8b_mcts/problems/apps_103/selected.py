def max_erasable_elements(n, array):
    if n == 1:
        return 0

    max_erase = 0
    current_length = 1

    for i in range(1, n):
        if array[i] == array[i - 1] + 1:
            current_length += 1
        else:
            max_erase = max(max_erase, current_length - 1)
            current_length = 1

    max_erase = max(max_erase, current_length - 1)

    return max_erase

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    array = list(map(int, data[1:n+1]))
    
    result = max_erasable_elements(n, array)
    print(result)