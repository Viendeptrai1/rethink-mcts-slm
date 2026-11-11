import sys

def max_rest_hours(n, schedule):
    max_rest = 0
    current_rest = 0
    
    # Check the rest hours in a single day
    for i in range(n):
        if schedule[i] == 1:
            current_rest += 1
        else:
            max_rest = max(max_rest, current_rest)
            current_rest = 0
    
    # Check the rest hours across the boundary between two days
    current_rest = 0
    for i in range(n):
        if schedule[i] == 1:
            current_rest += 1
        else:
            break
    
    for i in range(n - 1, -1, -1):
        if schedule[i] == 1:
            current_rest += 1
        else:
            break
    
    max_rest = max(max_rest, current_rest)
    
    return max_rest

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    schedule = list(map(int, data[1:]))
    
    result = max_rest_hours(n, schedule)
    print(result)

if __name__ == "__main__":
    main()