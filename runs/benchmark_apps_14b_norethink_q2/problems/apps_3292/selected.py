import sys
from collections import defaultdict
from math import factorial

MOD = 1_000_000_007

def count_orderings(n, names):
    # Build the prefix tree
    tree = defaultdict(list)
    for name in names:
        current = tree
        for char in name:
            if char not in current:
                current[char] = defaultdict(list)
            current = current[char]
        current['#'] = True  # Mark the end of a name

    # Function to calculate the number of valid orderings for a subtree
    def dfs(node):
        count = 1
        for child in node:
            if child != '#':
                child_count = dfs(node[child])
                count = (count * child_count) % MOD
                count = (count * factorial(len(node[child]))) % MOD
        return count

    # Start DFS from the root of the tree
    return dfs(tree)

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    names = data[1:]
    
    result = count_orderings(n, names)
    print(result)

if __name__ == "__main__":
    main()