import sys

def count_matching_ranges(n, numbers):
    count = 0
    prefix_sum = [0] * (n + 1)
    prefix_product = [1] * (n + 1)
    
    for i in range(1, n + 1):
        prefix_sum[i] = prefix_sum[i - 1] + numbers[i - 1]
        prefix_product[i] = prefix_product[i - 1] * numbers[i - 1]
    
    for start in range(1, n):
        for end in range(start + 1, n + 1):
            if prefix_sum[end] - prefix_sum[start] == prefix_product[end] // prefix_product[start]:
                count += 1
    
    return count

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