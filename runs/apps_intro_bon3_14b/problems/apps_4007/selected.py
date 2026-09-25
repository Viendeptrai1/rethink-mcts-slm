import sys

def solve():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    f = list(map(int, data[1:]))
    
    # Find indices of unknowns
    unknowns = [i for i in range(n) if f[i] == 0]
    
    # Find indices of knowns
    knowns = [i for i in range(n) if f[i] != 0]
    
    # Create a permutation of unknowns to assign to knowns
    from itertools import permutations
    perm = permutations(unknowns)
    
    # Try to find a valid permutation
    for p in perm:
        valid = True
        for i in range(len(knowns)):
            if f[knowns[i]] == p[i] + 1 or p[i] + 1 == knowns[i] + 1:
                valid = False
                break
        if valid:
            for i in range(len(unknowns)):
                f[p[i]] = unknowns[i] + 1
            break
    
    # Print the result
    print(" ".join(map(str, f)))

if __name__ == "__main__":
    solve()