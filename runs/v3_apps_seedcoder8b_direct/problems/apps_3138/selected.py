def count_matching_ranges(n, numbers):
    from collections import defaultdict

    # Dictionary to store the first occurrence of each prefix sum
    prefix_sum_index = defaultdict(list)
    prefix_sum_index[0].append(-1)  # To handle the case when the sum from the start is zero

    current_sum = 0
    count = 0

    for i in range(n):
        current_sum += numbers[i]

        # Check if there is a prefix sum that matches the current sum
        if current_sum in prefix_sum_index:
            # For each occurrence of this prefix sum, calculate the number of valid ranges
            for start_index in prefix_sum_index[current_sum]:
                if i - start_index >= 2:
                    count += 1

        # Store the current index for this prefix sum
        prefix_sum_index[current_sum].append(i)

    return count

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    numbers = list(map(int, data[1:n+1]))
    
    result = count_matching_ranges(n, numbers)
    print(result)

if __name__ == "__main__":
    main()