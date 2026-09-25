import sys

def can_complete_wall(n, a):
    min_height = min(a)
    if min_height == 0:
        return "NO"
    
    total_bricks_needed = sum(a) - n * min_height
    if total_bricks_needed % 2 == 0:
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