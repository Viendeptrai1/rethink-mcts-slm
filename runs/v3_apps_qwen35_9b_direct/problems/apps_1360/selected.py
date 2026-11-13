import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    
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
    
    # Sort exams based on the schedule date (a_i) first, then by early date (b_i)
    # This greedy approach works because we want to pick the earliest possible day
    # while maintaining non-decreasing order of recorded dates.
    # Sorting by 'a' ensures that if we process exams in this order, the recorded dates
    # will naturally be non-decreasing if we pick valid days.
    exams.sort(key=lambda x: (x[0], x[1]))
    
    current_day = 0
    for a, b in exams:
        # Try to take the exam on the early date b
        if b >= current_day:
            current_day = b
        else:
            # If early date is not possible (would break order), take on schedule date a
            # Since the list is sorted by 'a', and we know b < a, if b < current_day,
            # then a might still be >= current_day. We need to check.
            # Actually, since we sorted by 'a', the next 'a' is >= previous 'a' (which was >= current_day).
            # So taking 'a' is always safe for the order constraint.
            current_day = a
            
    print(current_day)

if __name__ == "__main__":
    solve()