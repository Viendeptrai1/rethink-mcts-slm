import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    
    if not data:
        return
    
    n = int(data[0])
    a = []
    idx = 1
    for i in range(n):
        a.append(int(data[idx]))
        idx += 1
    
    # We need to assign ratings b_i such that:
    # 1. b_i >= a_i for all i
    # 2. All b_i are distinct
    # 3. Sum(b_i) is minimized
    
    # Strategy:
    # Sort the users by their required rating a_i.
    # Iterate through the sorted users and assign the smallest possible value
    # that is >= a_i and distinct from all previously assigned values.
    
    # Store pairs of (required_rating, original_index)
    indexed_a = [(a[i], i) for i in range(n)]
    indexed_a.sort()
    
    result = [0] * n
    last_assigned = 0
    
    for req, orig_idx in indexed_a:
        # The new rating must be at least req and strictly greater than last_assigned
        # to ensure distinctness (since we process in increasing order of req)
        candidate = max(req, last_assigned + 1)
        result[orig_idx] = candidate
        last_assigned = candidate
    
    # Output the result sequence
    print(*(result))

if __name__ == "__main__":
    solve()