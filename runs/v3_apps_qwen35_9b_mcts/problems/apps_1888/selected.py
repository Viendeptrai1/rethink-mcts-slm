import sys

# Increase recursion depth just in case, though iterative approach is used below
sys.setrecursionlimit(2000)

def solve():
    # Read all input from stdin
    input_data = sys.stdin.read().split()
    
    if not input_data:
        return

    iterator = iter(input_data)
    
    try:
        n = int(next(iterator))
        m = int(next(iterator))
    except StopIteration:
        return

    # Calculate net balance for each person
    # balance[i] > 0 means person i should receive money
    # balance[i] < 0 means person i should give money
    balance = [0] * (n + 1)

    for _ in range(m):
        u = int(next(iterator))
        v = int(next(iterator))
        w = int(next(iterator))
        balance[u] -= w
        balance[v] += w

    # If there are no debts, the answer is 0
    if m == 0:
        print(0)
        return

    # We need to find connected components based on the original debt edges.
    # Within each component, the sum of positive balances must be paid out.
    # The minimum sum of debts for a component is the sum of all positive balances in that component.
    
    # Build adjacency list for the graph of people involved in debts
    adj = [[] for _ in range(n + 1)]
    involved = set()
    
    # Re-read the edges to build the graph (we already consumed them in the loop above, 
    # but we need to store them or re-parse. Since we used an iterator, let's reconstruct the edges list first).
    # Actually, let's just store edges during the first pass.
    
    edges = []
    # Reset iterator logic is not possible easily, so let's re-parse the input_data list directly.
    # We are at index 2 (after n and m).
    idx = 2
    while idx < len(input_data):
        u = int(input_data[idx])
        v = int(input_data[idx+1])
        w = int(input_data[idx+2])
        edges.append((u, v))
        adj[u].append(v)
        adj[v].append(u)
        involved.add(u)
        involved.add(v)
        idx += 3

    visited = [False] * (n + 1)
    total_min_debt = 0

    # Iterate over all people to find connected components
    for i in range(1, n + 1):
        if i in involved and not visited[i]:
            # Start BFS/DFS for this component
            component_positive_sum = 0
            stack = [i]
            visited[i] = True
            
            while stack:
                u = stack.pop()
                if balance[u] > 0:
                    component_positive_sum += balance[u]
                
                for v in adj[u]:
                    if not visited[v]:
                        visited[v] = True
                        stack.append(v)
            
            total_min_debt += component_positive_sum

    print(total_min_debt)

if __name__ == '__main__':
    solve()