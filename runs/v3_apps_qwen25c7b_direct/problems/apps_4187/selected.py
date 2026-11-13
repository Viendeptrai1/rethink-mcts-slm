def max_continuous_rests(n, schedule):
    max_rest = 0
    current_rest = 0
    
    for i in range(2 * n):
        if schedule[i % n] == 1:
            current_rest += 1
            max_rest = max(max_rest, current_rest)
        else:
            current_rest = 0
    
    return max_rest

# Example usage:
if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    schedule = list(map(int, data[1:]))
    
    result = max_continuous_rests(n, schedule)
    print(result)