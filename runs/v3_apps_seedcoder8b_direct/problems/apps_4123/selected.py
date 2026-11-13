def find_most_frequent_two_gram(n, s):
    from collections import defaultdict

    two_gram_count = defaultdict(int)

    for i in range(n - 1):
        two_gram = s[i:i+2]
        two_gram_count[two_gram] += 1

    max_count = 0
    most_frequent_two_gram = ""

    for two_gram, count in two_gram_count.items():
        if count > max_count:
            max_count = count
            most_frequent_two_gram = two_gram

    print(most_frequent_two_gram)

# Example usage:
# n = int(input().strip())
# s = input().strip()
# find_most_frequent_two_gram(n, s)