from collections import Counter

class Solution:
    def search(self, lst):
        freq = Counter(lst)
        for num in sorted(freq.keys(), reverse=True):
            if freq[num] >= num:
                return num
        return -1