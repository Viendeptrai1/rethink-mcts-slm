import sys

def find_permutation(n, p):
    # Create a list of tuples (p[i], i)
    indexed_p = list(enumerate(p, start=1))
    
    # Sort the list based on the values of p
    indexed_p.sort(key=lambda x: x[1])
    
    # Initialize the result permutation q
    q = [0] * (n + 1)
    
    # Try to construct q
    for i in range(1, n + 1):
        if q[i] != 0:
            continue
        cycle_length = 0
        x = i
        while q[x] == 0:
            q[x] = indexed_p[cycle_length][0]
            x = indexed_p[cycle_length][1]
            cycle_length += 1
        
        # If the cycle length is odd, it's impossible to form q^2 = p
        if cycle_length % 2 != 0:
            return [-1]
    
    # Return the permutation q without the 0th index
    return q[1:]

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    p = list(map(int, data[1:]))
    
    result = find_permutation(n, p)
    
    if result == [-1]:
        print(-1)
    else:
        print(" ".join(map(str, result)))

if __name__ == "__main__":
    main()