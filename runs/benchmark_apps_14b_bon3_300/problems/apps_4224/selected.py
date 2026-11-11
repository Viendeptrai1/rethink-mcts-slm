import sys

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    a = list(map(int, data[1:]))
    
    max_operations = 0
    
    for ai in a:
        operations = 0
        while ai % 2 == 0:
            ai //= 2
            operations += 1
        while ai % 3 == 0:
            ai //= 3
            operations += 1
        if ai == 1:
            max_operations = max(max_operations, operations)
    
    print(max_operations)

if __name__ == "__main__":
    main()