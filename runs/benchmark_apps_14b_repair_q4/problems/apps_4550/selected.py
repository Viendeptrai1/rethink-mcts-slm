import sys

def main():
    a, b, c = map(int, sys.stdin.readline().split())
    total_candies = a + b + c
    
    if total_candies % 2 == 0:
        target = total_candies // 2
        if a <= target and b <= target and c <= target:
            if a + b == target or a + c == target or b + c == target or a == target or b == target or c == target:
                print("Yes")
            else:
                print("No")
        else:
            print("No")
    else:
        print("No")

if __name__ == "__main__":
    main()