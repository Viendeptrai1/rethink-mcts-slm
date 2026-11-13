from collections import Counter

class Solution:
    def histogram(self, test):
        if not test:
            return {}
        
        words = test.split()
        counts = Counter(words)
        max_count = max(counts.values(), default=0)
        return {word: count for word, count in counts.items() if count == max_count}

# For call-based execution
def histogram(test):
    return Solution().histogram(test)