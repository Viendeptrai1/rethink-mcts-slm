import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    v1 = int(input_data[0])
    v2 = int(input_data[1])
    t = int(input_data[2])
    d = int(input_data[3])
    
    # There are t seconds, so we have speeds at second 1, 2, ..., t.
    # Let s[i] be the speed at second i (1-indexed).
    # We know:
    # s[1] = v1
    # s[t] = v2
    # |s[i] - s[i-1]| <= d for all i from 2 to t
    # We want to maximize sum(s[i]) for i from 1 to t.
    
    # For any second i, the maximum possible speed s[i] is constrained by:
    # 1. Starting from v1: s[i] <= v1 + (i - 1) * d
    # 2. Ending at v2: s[i] <= v2 + (t - i) * d
    # The actual maximum speed at second i is the minimum of these two constraints.
    
    total_distance = 0
    for i in range(1, t + 1):
        max_from_start = v1 + (i - 1) * d
        max_from_end = v2 + (t - i) * d
        s_i = min(max_from_start, max_from_end)
        total_distance += s_i
        
    print(total_distance)

if __name__ == "__main__":
    solve()