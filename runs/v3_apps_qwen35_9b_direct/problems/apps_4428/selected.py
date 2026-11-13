import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    
    if not data:
        return
    
    n = int(data[0])
    d = []
    for i in range(n):
        d.append(int(data[1 + i]))
    
    # Use two pointers approach
    # left pointer starts at 0, right pointer starts at n-1
    # We maintain current sums for the left part and right part
    
    left_sum = 0
    right_sum = 0
    left_idx = 0
    right_idx = n - 1
    
    max_sum = 0
    
    # We will move pointers to try to match sums
    # Since all d[i] >= 1, sums are strictly increasing as we add elements
    
    # Strategy:
    # If left_sum < right_sum, we need to add more elements to the left part
    # If left_sum > right_sum, we need to add more elements to the right part
    # If equal, we record the sum and try to find a larger one
    
    while left_idx <= right_idx:
        if left_sum == right_sum:
            if left_sum > max_sum:
                max_sum = left_sum
            # Try to extend both sides to see if we can get a larger equal sum
            # But we must be careful not to cross or overlap in a way that invalidates the split
            # Actually, if sums are equal, we can try to extend left and right independently
            # However, the standard two-pointer for this problem works by:
            # If left < right, add from left
            # If left > right, add from right
            # If equal, record and then add from left (or right) to continue searching
            
            # Let's add from left to try to find a larger match
            left_sum += d[left_idx]
            left_idx += 1
        elif left_sum < right_sum:
            left_sum += d[left_idx]
            left_idx += 1
        else: # left_sum > right_sum
            right_sum += d[right_idx]
            right_idx -= 1
            
    print(max_sum)

if __name__ == "__main__":
    solve()