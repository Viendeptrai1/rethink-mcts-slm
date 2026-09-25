import sys

def main():
    import sys
    n = int(sys.stdin.readline().strip())
    a = list(map(int, sys.stdin.readline().strip().split()))
    
    result = 0
    for num in a:
        result ^= num
    
    print(result)

if __name__ == "__main__":
    main()