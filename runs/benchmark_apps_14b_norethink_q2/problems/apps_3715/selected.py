import sys

def min_rest_days(n, activities):
    def backtrack(day, last_activity, rest_days):
        if day == n:
            return rest_days
        
        min_rest = float('inf')
        
        # Option 1: Rest
        min_rest = min(min_rest, backtrack(day + 1, -1, rest_days + 1))
        
        # Option 2: Write contest if possible
        if activities[day] in [1, 3] and last_activity != 1:
            min_rest = min(min_rest, backtrack(day + 1, 1, rest_days))
        
        # Option 3: Do sport if possible
        if activities[day] in [2, 3] and last_activity != 2:
            min_rest = min(min_rest, backtrack(day + 1, 2, rest_days))
        
        return min_rest
    
    return backtrack(0, -1, 0)

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    activities = list(map(int, data[1:]))
    
    result = min_rest_days(n, activities)
    print(result)

if __name__ == "__main__":
    main()