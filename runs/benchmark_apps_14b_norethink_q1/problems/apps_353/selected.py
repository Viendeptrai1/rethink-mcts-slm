import sys

def main():
    import sys
    n = int(sys.stdin.readline().strip())
    moon_sizes = list(map(int, sys.stdin.readline().strip().split()))
    
    if n == 1:
        print(-1)
        return
    
    if moon_sizes[-1] < moon_sizes[-2]:
        print("DOWN")
    elif moon_sizes[-1] > moon_sizes[-2]:
        print("UP")
    else:
        print(-1)

if __name__ == "__main__":
    main()