import sys

def is_sorted(arr):
    for i in range(len(arr) - 1):
        if arr[i] > arr[i + 1]:
            return False
    return True

def thanos_sort_max_length(arr):
    n = len(arr)
    if n == 0:
        return 0
    if is_sorted(arr):
        return n
    
    half = n // 2
    left_half = arr[:half]
    right_half = arr[half:]
    
    return max(thanos_sort_max_length(left_half), thanos_sort_max_length(right_half))

def main():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    n = int(input_data[0])
    a = []
    for i in range(n):
        a.append(int(input_data[1 + i]))
    
    result = thanos_sort_max_length(a)
    print(result)

if __name__ == "__main__":
    main()