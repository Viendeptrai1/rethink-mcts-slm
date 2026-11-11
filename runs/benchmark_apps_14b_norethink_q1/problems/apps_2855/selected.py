import sys
from collections import defaultdict

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    index = 0
    N = int(data[index])
    M = int(data[index + 1])
    index += 2
    
    graph = defaultdict(list)
    for _ in range(M):
        K = int(data[index])
        L = int(data[index + 1])
        graph[K].append(L)
        graph[L].append(K)
        index += 2
    
    # Initialize the expected times array
    E = [0] * N
    E[N - 1] = 0  # Exit is at N-1, so it takes 0 time to get out from there
    
    # Create a list of nodes excluding the exit node
    nodes = list(range(N - 1))
    
    # Iterate until the values converge
    while True:
        changed = False
        for i in nodes:
            new_Ei = 1 + sum(E[j] for j in graph[i]) / len(graph[i])
            if abs(new_Ei - E[i]) > 1e-9:
                changed = True
            E[i] = new_Ei
        if not changed:
            break
    
    print(f"{E[0]:.6f}")

if __name__ == "__main__":
    main()