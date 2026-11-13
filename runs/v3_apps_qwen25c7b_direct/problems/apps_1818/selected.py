from collections import Counter

def count_pairs(n, a):
    def f(x):
        if x == 0:
            return 0
        elif x % 2 == 0:
            return f(x // 2)
        else:
            return f((x - 1) // 2) + 1
    
    counts = Counter()
    result = 0
    
    for num in a:
        result += counts[f(num)]
        counts[f(num)] += 1
    
    return result

# Read input
n = int(input())
a = list(map(int, input().split()))

# Output the result
print(count_pairs(n, a))