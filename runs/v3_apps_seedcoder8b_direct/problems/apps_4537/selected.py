def main():
    import sys
    input = sys.stdin.read
    data = input().strip()
    A, B = map(int, data.split())
    
    result = max(A + B, A - B, A * B)
    print(result)

if __name__ == "__main__":
    main()