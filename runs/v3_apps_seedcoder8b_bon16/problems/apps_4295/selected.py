def main():
    import sys
    input = sys.stdin.read
    data = input().strip()
    
    # Parse the input
    N, K = map(int, data.split())
    
    # Calculate the minimum possible value of N
    min_value = min(N, abs(N - 2 * K))
    
    # Print the result
    print(min_value)

if __name__ == "__main__":
    main()