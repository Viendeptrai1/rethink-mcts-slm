from collections import defaultdict

def max_two_gram(s):
    n = len(s)
    two_gram_count = defaultdict(int)
    
    for i in range(n - 1):
        two_gram = s[i:i+2]
        two_gram_count[two_gram] += 1
    
    max_count = 0
    result = ''
    for two_gram, count in two_gram_count.items():
        if count > max_count or (count == max_count and two_gram < result):
            max_count = count
            result = two_gram
    
    return result

# Input handling
n = int(input().strip())
s = input().strip()

# Output the result
print(max_two_gram(s))