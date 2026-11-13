def main():
    import sys
    input = sys.stdin.read
    data = input().strip()
    A, B = map(int, data.split())
    
    # Check if the product is odd
    if (A * B) % 2 == 1:
        print("Yes")
    else:
        print("No")

if __name__ == "__main__":
    main()