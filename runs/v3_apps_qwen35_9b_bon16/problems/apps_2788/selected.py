import sys

def solve():
    data = sys.stdin.read().split()
    if not data:
        return
    
    iterator = iter(data)
    n = int(next(iterator))
    groups = []
    for _ in range(n):
        groups.append(int(next(iterator)))
    
    k = int(next(iterator))
    x = int(next(iterator))
    a = int(next(iterator))
    b = int(next(iterator))
    
    total_capacity = k * x
    
    # Generate all possible sums using groups without exceeding total_capacity
    # Since n <= 1000 and group sizes are small (<=100), max sum could be 1000*100 = 100,000
    # We can use a set to track reachable sums up to total_capacity
    
    reachable = {0}
    for s in groups:
        new_reachable = set()
        for current_sum in reachable:
            new_sum = current_sum + s
            if new_sum <= total_capacity:
                new_reachable.add(new_sum)
        reachable.update(new_reachable)
    
    # Find the maximum sum that satisfies:
    # 1. sum == some multiple of x (no wasted lunches)
    # 2. a <= sum <= b
    
    max_students = -1
    found = False
    
    for s in reachable:
        if s == 0:
            continue
        if s > total_capacity:
            continue
        if s % x == 0:
            if a <= s <= b:
                found = True
                if s > max_students:
                    max_students = s
    
    if found:
        print(max_students)
    else:
        print("impossible")

if __name__ == "__main__":
    solve()