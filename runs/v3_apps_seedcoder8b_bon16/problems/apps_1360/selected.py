import sys

def solve():
    n = int(sys.stdin.readline())
    exams = [list(map(int, sys.stdin.readline().split())) for _ in range(n)]
    
    exams.sort(key=lambda x: (x[1], -x[0]))
    
    last_day = 0
    for schedule, early in exams:
        if last_day >= schedule:
            last_day = schedule
        else:
            last_day = early
    
    print(last_day)

if __name__ == "__main__":
    solve()