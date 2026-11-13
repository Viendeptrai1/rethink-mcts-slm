def most_frequent_two_gram(n, s):
    from collections import defaultdict
    
    # Dictionary to store the frequency of each two-gram
    freq = defaultdict(int)
    
    # Iterate through the string and count the frequency of each two-gram
    for i in range(n - 1):
        two_gram = s[i:i+2]
        freq[two_gram] += 1
    
    # Find the maximum frequency
    max_freq = max(freq.values())
    
    # Collect all two-grams with the maximum frequency
    max_two_grams = [two_gram for two_gram, count in freq.items() if count == max_freq]
    
    # Return the lexicographically smallest two-gram
    return min(max_two_grams)

# Read input
n = int(input().strip())
s = input().strip()

# Output the result
print(most_frequent_two_gram(n, s))