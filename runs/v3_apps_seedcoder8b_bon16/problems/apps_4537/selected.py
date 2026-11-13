def main():
    import sys
    input = sys.stdin.read
    data = input().strip()
    A, B = map(int, data.split())
    
    # Calculate the values
    sum_ab = A + B
    diff_ab = A - B
    prod_ab = A * B
    
    # Find the maximum value
    max_value = max(sum_ab, diff_ab, prod_ab)
    
    # Print the result
    print(max_value)

if __name__ == "__main__":
    main()