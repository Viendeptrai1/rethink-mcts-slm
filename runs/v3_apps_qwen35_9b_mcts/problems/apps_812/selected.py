import sys

def is_ap(arr):
    n = len(arr)
    if n <= 2:
        return True
    d = arr[1] - arr[0]
    for i in range(2, n):
        if arr[i] - arr[i-1] != d:
            return False
    return True

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    n = int(input_data[0])
    b = []
    for i in range(n):
        b.append(int(input_data[1 + i]))
    
    # Sort the array to easily check AP properties
    sorted_b = sorted(b)
    
    # Helper to check if removing element at index 'idx' from sorted_b forms an AP
    def check_remove(idx):
        if idx == 0:
            return is_ap(sorted_b[1:])
        if idx == n - 1:
            return is_ap(sorted_b[:-1])
        return is_ap(sorted_b[:idx] + sorted_b[idx+1:])
    
    # Case 1: If the sorted array is already an AP
    if is_ap(sorted_b):
        # We can remove the first element (index 0 in 1-based is 1)
        # Or the last element. The problem asks for any index j.
        # Since we need to return the original index, we need to map back.
        # However, if the array is already an AP, removing the first element of the sorted array
        # corresponds to removing the smallest element.
        # Let's find the original index of the smallest element.
        min_val = sorted_b[0]
        # Find the first occurrence of min_val in original b to return a valid index
        for i in range(n):
            if b[i] == min_val:
                print(i + 1)
                return
        # Fallback (should not happen if logic is correct)
        print(1)
        return

    # Case 2: Try removing the first element of the sorted array
    if check_remove(0):
        min_val = sorted_b[0]
        for i in range(n):
            if b[i] == min_val:
                print(i + 1)
                return

    # Case 3: Try removing the last element of the sorted array
    if check_remove(n - 1):
        max_val = sorted_b[-1]
        for i in range(n):
            if b[i] == max_val:
                print(i + 1)
                return

    # Case 4: Try removing an element in the middle
    # If the array is not an AP, there must be a gap or a duplicate issue.
    # We look for the first index i where the difference changes.
    # In a valid AP of length n-1, the total range (max - min) must be divisible by n-2.
    # But a simpler approach is to scan for the first deviation.
    
    # Find the first index where the difference is not constant
    d1 = sorted_b[1] - sorted_b[0]
    for i in range(2, n):
        d2 = sorted_b[i] - sorted_b[i-1]
        if d2 != d1:
            # We found a deviation at index i (between i-1 and i)
            # The problematic element could be sorted_b[i-1] or sorted_b[i]
            # Try removing sorted_b[i-1]
            if check_remove(i - 1):
                val = sorted_b[i-1]
                for idx in range(n):
                    if b[idx] == val:
                        print(idx + 1)
                        return
            # Try removing sorted_b[i]
            if check_remove(i):
                val = sorted_b[i]
                for idx in range(n):
                    if b[idx] == val:
                        print(idx + 1)
                        return
            break
    else:
        # No deviation found in the loop, but we already checked is_ap at the start.
        # This part should theoretically not be reached if is_ap was correct,
        # unless n=2 which is handled by is_ap returning True.
        pass

    # If no solution found
    print(-1)

if __name__ == "__main__":
    solve()