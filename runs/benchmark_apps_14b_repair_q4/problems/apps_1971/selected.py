import sys

def find_permutation(n, p):
    # Create a list to store the result permutation q
    q = [-1] * n
    
    # Create a list to keep track of visited elements
    visited = [False] * n
    
    # Iterate over each element in the permutation p
    for i in range(n):
        if not visited[i]:
            cycle = []
            x = i
            while not visited[x]:
                visited[x] = True
                cycle.append(x)
                x = p[x] - 1
            
            # Check if the length of the cycle is even
            if len(cycle) % 2 != 0:
                return [-1]
            
            # Pair up elements in the cycle to form q
            mid = len(cycle) // 2
            for j in range(mid):
                q[cycle[j]] = cycle[(j + mid) % len(cycle)] + 1
                q[cycle[(j + mid) % len(cycle)]] = cycle[j] + 1
    
    return q

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