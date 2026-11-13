def main():
    import sys
    input = sys.stdin.read
    data = input().strip()
    a, b, c = map(int, data.split())
    
    total_candies = a + b + c
    
    if total_candies % 2 == 0:
        print("Yes")
    else:
        print("No")

if __name__ == "__main__":
    main()