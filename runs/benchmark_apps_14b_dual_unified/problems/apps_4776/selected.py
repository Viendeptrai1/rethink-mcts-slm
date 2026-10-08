def count_free_food_days(N, events):
    days = [0] * 365
    for s_i, t_i in events:
        for day in range(s_i - 1, t_i):
            days[day] += 1
    return sum(1 for count in days if count > 0)

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    events = []
    index = 1
    for _ in range(N):
        s_i = int(data[index])
        t_i = int(data[index + 1])
        events.append((s_i, t_i))
        index += 2
    
    result = count_free_food_days(N, events)
    print(result)