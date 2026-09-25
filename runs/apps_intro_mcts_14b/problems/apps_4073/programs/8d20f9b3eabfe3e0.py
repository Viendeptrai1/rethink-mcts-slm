import sys

def main():
    import sys
    n = int(sys.stdin.readline().strip())
    a = list(map(int, sys.stdin.readline().strip().split()))
    
    count = sum(1 for x in a if x >= 4)
    print(count)

if __name__ == "__main__":
    main()