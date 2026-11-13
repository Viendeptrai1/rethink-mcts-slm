def main():
    import sys
    input = sys.stdin.read
    data = input().strip()
    K, X = map(int, data.split())
    
    total_value = K * 500
    if total_value >= X:
        print("Yes")
    else:
        print("No")

if __name__ == "__main__":
    main()