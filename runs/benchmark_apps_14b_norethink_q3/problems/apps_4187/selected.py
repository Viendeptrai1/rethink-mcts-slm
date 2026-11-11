import sys

def max_rest_period(n, schedule):
    max_rest = 0
    current_rest = 0
    
    # Check rest periods within a single day
    for i in range(n):
        if schedule[i] == 1:
            current_rest += 1
        else:
            max_rest = max(max_rest, current_rest)
            current_rest = 0
    
    # Check rest period spanning across midnight
    if schedule[-1] == 1 and schedule[0] == 1:
        max_rest = max(max_rest, current_rest + 1)
    
    return max_rest

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    schedule = list(map(int, data[1:]))
    
    result = max_rest_period(n, schedule)
    print(result)

if __name__ == "__main__":
    main()