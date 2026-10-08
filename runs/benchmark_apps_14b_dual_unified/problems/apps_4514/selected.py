import sys
from collections import defaultdict

def main():
    import sys
    import threading
    
    def solve():
        import sys
        import threading
        
        def dfs(node, parent):
            order.append(node)
            for child in adj[node]:
                if child != parent:
                    dfs(child, node)
        
        def find_kth_officer(u, k):
            order = []
            dfs(u, -1)
            if k <= len(order):
                return order[k - 1]
            else:
                return -1
        
        n, q = map(int, sys.stdin.readline().split())
        parents = list(map(int, sys.stdin.readline().split()))
        
        adj = defaultdict(list)
        for i in range(1, n):
            adj[parents[i]].append(i + 1)
            adj[i + 1].append(parents[i])
        
        results = []
        for _ in range(q):
            u, k = map(int, sys.stdin.readline().split())
            results.append(find_kth_officer(u, k))
        
        for result in results:
            print(result)
    
    threading.Thread(target=solve).start()

if __name__ == "__main__":
    main()