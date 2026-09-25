import sys

def can_complete_wall(n, heights):
    min_height = min(heights)
    max_height = max(heights)
    
    # Check if all parts can be raised to the minimum height
    for height in heights:
        if (height - min_height) % 2 != 0:
            return "NO"
    
    return "YES"

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    heights = list(map(int, data[1:]))
    
    result = can_complete_wall(n, heights)
    print(result)

if __name__ == "__main__":
    main()