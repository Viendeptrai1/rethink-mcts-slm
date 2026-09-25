import sys

def can_complete_wall(n, a):
    # Check if all elements in the list are the same
    if len(set(a)) == 1:
        return "YES"
    
    # Check if the difference between max and min height is even
    max_height = max(a)
    min_height = min(a)
    
    if (max_height - min_height) % 2 == 0:
        return "YES"
    else:
        return "NO"

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    a = list(map(int, data[1:]))
    
    result = can_complete_wall(n, a)
    print(result)

if __name__ == "__main__":
    main()