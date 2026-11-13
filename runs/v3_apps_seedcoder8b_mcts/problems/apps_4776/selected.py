def count_days_with_free_food():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    days_with_food = set()
    
    index = 1
    for _ in range(N):
        s_i = int(data[index])
        t_i = int(data[index + 1])
        index += 2
        for day in range(s_i, t_i + 1):
            days_with_food.add(day)
    
    return len(days_with_food)

# Call the function and print the result
print(count_days_with_free_food())