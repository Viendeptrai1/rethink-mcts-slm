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
    
    # Sort exams by scheduled date (a_i), then by early date (b_i)
    exams.sort(key=lambda x: (x[0], x[1]))
    
    current_day = 0
    
    for a, b in exams:
        # Try to take the exam on the early date b if it's >= current_day
        if b >= current_day:
            current_day = b
        else:
            # Otherwise, take it on the scheduled date a
            current_day = a
            
    print(current_day)

if __name__ == "__main__":
    solve()