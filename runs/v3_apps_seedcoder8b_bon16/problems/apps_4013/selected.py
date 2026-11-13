def min_possible_instability(n, a):
    # Sort the array to easily find the maximum and minimum elements
    a.sort()
    
    # The potential minimum instability is calculated by two cases:
    # 1. Remove the maximum element
    # 2. Remove the minimum element
    
    # Case 1: Remove the maximum element
    max_except_one = a[-2] - a[0]
    
    # Case 2: Remove the minimum element
    min_except_one = a[-1] - a[1]
    
    # The minimum instability will be the smallest of these two cases
    return min(max_except_one, min_except_one)

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    a = list(map(int, data[1:]))
    
    print(min_possible_instability(n, a))