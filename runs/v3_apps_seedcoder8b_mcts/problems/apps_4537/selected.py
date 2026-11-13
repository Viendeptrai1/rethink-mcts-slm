def main():
    import sys
    input = sys.stdin.read
    data = input().strip()
    A, B = map(int, data.split())
    
    sum_ab = A + B
    diff_ab = A - B
    prod_ab = A * B
    
    largest = max(sum_ab, diff_ab, prod_ab)
    print(largest)

if __name__ == "__main__":
    main()