def count_free_food_days(N, events):
    # Create a set to store unique days with free food
    free_food_days = set()
    
    # Iterate over each event and add its days to the set
    for start, end in events:
        free_food_days.update(range(start, end + 1))
    
    # Return the number of unique days with free food
    return len(free_food_days)

# Example usage:
if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    events = [(int(data[2 * i + 1]), int(data[2 * i + 2])) for i in range(N)]
    
    result = count_free_food_days(N, events)
    print(result)