def main():
    import sys
    input = sys.stdin.read
    data = input().strip()
    K, X = map(int, data.split())
    
    if K * 500 >= X:
        print("Yes")
    else:
        print("No")

if __name__ == "__main__":
    main()