import sys
from itertools import permutations

def is_substring(a, b):
    return a in b

def can_reorder(strings):
    n = len(strings)
    for perm in permutations(range(n)):
        valid = True
        for i in range(1, n):
            if not is_substring(strings[perm[i]], strings[perm[i-1]]):
                valid = False
                break
        if valid:
            return ["YES"] + [strings[perm[i]] for i in range(n)]
    return ["NO"]

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    strings = data[1:]
    
    result = can_reorder(strings)
    print("\n".join(result))

if __name__ == "__main__":
    main()