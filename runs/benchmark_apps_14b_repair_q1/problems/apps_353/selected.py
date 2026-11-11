import sys

def main():
    import sys
    n = int(sys.stdin.readline().strip())
    a = list(map(int, sys.stdin.readline().strip().split()))
    
    if n == 1:
        print(-1)
        return
    
    if a[-1] < a[-2]:
        print("DOWN")
    elif a[-1] > a[-2]:
        print("UP")
    else:
        print(-1)

if __name__ == "__main__":
    main()