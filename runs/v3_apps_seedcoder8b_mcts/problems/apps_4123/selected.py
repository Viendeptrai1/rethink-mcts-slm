def find_most_frequent_two_gram(n, s):
    from collections import defaultdict

    two_gram_count = defaultdict(int)

    # Count occurrences of each two-gram
    for i in range(n - 1):
        two_gram = s[i:i+2]
        two_gram_count[two_gram] += 1

    # Find the two-gram with the maximum count
    max_count = max(two_gram_count.values())
    most_frequent_two_grams = [
        two_gram for two_gram, count in two_gram_count.items() if count == max_count
    ]

    # Return the lexicographically smallest two-gram
    return min(most_frequent_two_grams)

# Read input
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
s = data[1]

# Find and print the most frequent two-gram
print(find_most_frequent_two_gram(n, s))