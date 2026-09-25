import sys

def can_complete_wall(n, a):
    # Find the minimum height in the wall
    min_height = min(a)
    
    # Check if we can make all parts of the wall reach the minimum height
    for i in range(1, n):
        if a[i] < min_height or (a[i] > min_height and a[i] != a[i - 1]):
            return "NO"
    
    return "YES"

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