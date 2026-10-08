import sys

def main():
    import sys
    n = int(sys.stdin.readline().strip())
    a = list(map(int, sys.stdin.readline().strip().split()))
    
    if n == 1:
        print(-1)
        return
    
    if n == 2:
        if a[0] < a[1]:
            print("UP")
        elif a[0] > a[1]:
            print("DOWN")
        else:
            print(-1)
        return
    
    if a[-3] < a[-2] < a[-1]:
        print("UP")
    elif a[-3] > a[-2] > a[-1]:
        print("DOWN")
    else:
        print(-1)

if __name__ == "__main__":
    main()