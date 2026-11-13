from typing import List

def count_matching_ranges(n: int, numbers: List[int]) -> int:
    count = 0
    prefix_sum = [0] * (n + 1)
    prefix_product = [1] * (n + 1)
    
    for i in range(1, n + 1):
        prefix_sum[i] = prefix_sum[i - 1] + numbers[i - 1]
        prefix_product[i] = prefix_product[i - 1] * numbers[i - 1]
    
    for start in range(n):
        for end in range(start + 1, n):
            if prefix_sum[end + 1] - prefix_sum[start] == prefix_product[end + 1] // prefix_product[start]:
                count += 1
    
    return count

# Example usage:
if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    n = int(data[0])
    numbers = list(map(int, data[1:]))
    result = count_matching_ranges(n, numbers)
    print(result)