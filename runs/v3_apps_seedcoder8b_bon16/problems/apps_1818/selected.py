def count_equal_f_function_pairs(n, sequence):
    def f(x):
        result = 0
        while x > 0:
            if x % 2 == 1:
                result += 1
            x //= 2
        return result

    # Calculate f(a_i) for all a_i in the sequence
    f_values = [f(a_i) for a_i in sequence]

    # Dictionary to count occurrences of each f(a_i) value
    count_map = {}
    for value in f_values:
        if value in count_map:
            count_map[value] += 1
        else:
            count_map[value] = 1

    # Calculate the number of pairs (i, j) with f(a_i) == f(a_j)
    pairs_count = 0
    for count in count_map.values():
        if count > 1:
            # If there are `count` elements with the same f value,
            # the number of ways to pick 2 elements (i, j) is count choose 2
            pairs_count += count * (count - 1) // 2

    return pairs_count

# Example usage:
if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    sequence = list(map(int, data[1:n+1]))
    
    result = count_equal_f_function_pairs(n, sequence)
    print(result)