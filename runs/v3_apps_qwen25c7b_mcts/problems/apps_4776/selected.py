def count_free_food_days(N, events):
    free_food_days = set()
    
    for start, end in events:
        for day in range(start, end + 1):
            free_food_days.add(day)
    
    return len(free_food_days)

# Example usage:
if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    events = [(int(data[2*i+1]), int(data[2*i+2])) for i in range(N)]
    
    result = count_free_food_days(N, events)
    print(result)