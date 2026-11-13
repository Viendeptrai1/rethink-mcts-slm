def main():
    import sys
    input = sys.stdin.read
    data = input().strip()
    A, B = map(int, data.split())
    
    # Check if any of A, B, or their product is odd
    if A % 2 == 1 or B % 2 == 1:
        print("Yes")
    else:
        print("No")

if __name__ == "__main__":
    main()