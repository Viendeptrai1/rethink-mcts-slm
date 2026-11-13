def solve():
    N = int(input())
    events = [list(map(int, input().split())) for _ in range(N)]
    
    food_days = set()
    for start, end in events:
        food_days.update(range(start, end + 1))
    
    print(len(food_days))

if __name__ == "__main__":
    solve()