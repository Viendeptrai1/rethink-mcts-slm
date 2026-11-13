def max_two_gram(s):
    n = len(s)
    count = {}
    
    # Count occurrences of each two-gram
    for i in range(n - 1):
        two_gram = s[i:i+2]
        if two_gram in count:
            count[two_gram] += 1
        else:
            count[two_gram] = 1
    
    # Find the two-gram with the maximum count
    max_count = 0
    max_two_gram = ""
    for two_gram, cnt in count.items():
        if cnt > max_count:
            max_count = cnt
            max_two_gram = two_gram
    
    return max_two_gram

# Read input
n = int(input())
s = input().strip()

# Output the result
print(max_two_gram(s))