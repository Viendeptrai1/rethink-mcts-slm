import sys

def solve():
    input = sys.stdin.read
    data = input().strip().split()
    if not data:
        return
    
    n = int(data[0])
    exams = []
    idx = 1
    for _ in range(n):
        a = int(data[idx])
        b = int(data[idx+1])
        exams.append((a, b))
        idx += 2
    
    # Sort exams based on schedule date a_i first, then early date b_i
    # This greedy approach works because we want to pick the earliest possible day
    # while maintaining non-decreasing order of recorded dates (which are always a_i).
    # If we sort by a_i, we process exams in the order their recorded dates appear.
    # Then we greedily pick the smallest valid day (either b_i or a_i) that is >= previous day.
    exams.sort()
    
    current_day = 0
    for a, b in exams:
        # We need to pick a day >= current_day.
        # Options are b and a. Since b < a, we prefer b if b >= current_day.
        if b >= current_day:
            current_day = b
        else:
            # If b is too early, we must take it on day a.
            # Since the list is sorted by a, a is guaranteed to be >= previous a's.
            # Also, since b < a and b < current_day, it's possible a >= current_day.
            # In a valid configuration where a solution exists, a will be >= current_day.
            current_day = a
            
    print(current_day)

if __name__ == "__main__":
    solve()