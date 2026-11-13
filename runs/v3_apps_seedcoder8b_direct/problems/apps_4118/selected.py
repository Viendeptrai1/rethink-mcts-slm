def main():
    import sys
    input = sys.stdin.read
    data = input().strip()
    A, B = map(int, data.split())
    
    if 1 <= A <= 9 and 1 <= B <= 9:
        print(A * B)
    else:
        print(-1)

if __name__ == "__main__":
    main()