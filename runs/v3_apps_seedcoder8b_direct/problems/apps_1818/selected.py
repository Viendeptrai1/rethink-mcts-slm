def count_equal_f_values(n, sequence):
    from collections import defaultdict

    # Function to calculate f(x)
    def f(x):
        result = 0
        while x > 0:
            if x % 2 == 1:
                result += 1
            x //= 2
        return result

    # Dictionary to count occurrences of each f(a_i)
    f_count = defaultdict(int)

    # Calculate f(a_i) for each element in the sequence and count occurrences
    for number in sequence:
        f_value = f(number)
        f_count[f_value] += 1

    # Calculate the number of pairs (i, j) with f(a_i) = f(a_j)
    pairs_count = 0
    for count in f_count.values():
        if count > 1:
            # If there are 'count' elements with the same f value,
            # the number of ways to pick 2 indices (i, j) is count choose 2
            pairs_count += count * (count - 1) // 2

    return pairs_count

# Read input
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
sequence = list(map(int, data[1:n+1]))

# Get the result and print it
result = count_equal_f_values(n, sequence)
print(result)