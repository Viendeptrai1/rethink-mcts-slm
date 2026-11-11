def count_matching_ranges(n, numbers):
    total_ways = 0
    
    # Calculate prefix sums and prefix products
    prefix_sums = [0] * (n + 1)
    prefix_products = [1] * (n + 1)
    
    for i in range(1, n + 1):
        prefix_sums[i] = prefix_sums[i - 1] + numbers[i - 1]
        prefix_products[i] = prefix_products[i - 1] * numbers[i - 1]
    
    # Check each subarray
    for i in range(1, n + 1):
        for j in range(i + 1, n + 1):
            current_sum = prefix_sums[j] - prefix_sums[i - 1]
            current_product = prefix_products[j] // prefix_products[i - 1]
            if current_sum == current_product:
                total_ways += 1
    
    return total_ways

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    numbers = list(map(int, data[1:]))
    
    result = count_matching_ranges(n, numbers)
    print(result)

if __name__ == "__main__":
    main()