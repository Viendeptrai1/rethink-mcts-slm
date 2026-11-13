def count_days_with_free_food():
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
    
    # Create a set to store unique days with free food
    days_with_free_food = set()
    
    # Iterate over each event and add its days to the set
    for s_i, t_i in events:
        for day in range(s_i, t_i + 1):
            days_with_free_food.add(day)
    
    # The number of unique days is the answer
    print(len(days_with_free_food))