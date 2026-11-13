def find_most_frequent_two_gram(n, s):
    from collections import defaultdict

    # Dictionary to store counts of each two-gram
    two_gram_counts = defaultdict(int)

    # Iterate over the string to count two-grams
    for i in range(n - 1):
        two_gram = s[i:i + 2]
        two_gram_counts[two_gram] += 1

    # Find the two-gram with the maximum count
    max_count = 0
    result_two_gram = ""
    for two_gram, count in two_gram_counts.items():
        if count > max_count:
            max_count = count
            result_two_gram = two_gram

    # Print the result
    print(result_two_gram)

# Read input
import sys
input = sys.stdin.read
data = input().strip().split()
n = int(data[0])
s = data[1]

# Find and print the most frequent two-gram
find_most_frequent_two_gram(n, s)