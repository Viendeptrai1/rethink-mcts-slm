import sys

def main():
    import sys
    import math
    
    def max_operations(N, a):
        operations = 0
        for num in a:
            while num % 2 == 0:
                num //= 2
                operations += 1
            while num % 3 == 0:
                num //= 3
                operations += 1
        return operations
    
    N = int(sys.stdin.readline().strip())
    a = list(map(int, sys.stdin.readline().strip().split()))
    
    result = max_operations(N, a)
    print(result)

if __name__ == "__main__":
    main()