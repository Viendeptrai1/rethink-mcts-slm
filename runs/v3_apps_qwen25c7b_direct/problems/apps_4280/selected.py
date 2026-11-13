import sys
from collections import defaultdict

def read_input():
    input = sys.stdin.read
    data = input().split()
    index = 0
    def next_int():
        nonlocal index
        result = int(data[index])
        index += 1
        return result
    n = next_int()
    k = next_int()
    roads = []
    for _ in range(n - 1):
        x = next_int()
        y = next_int()
        roads.append((x, y))
    return n, k, roads

def solve(n, k, roads):
    # Create adjacency list
    adj_list = defaultdict(list)
    for u, v in roads:
        adj_list[u].append(v)
        adj_list[v].append(u)
    
    # Function to check if a given number of companies works
    def can_partition(r):
        # Initialize company assignments
        company = [0] * (n + 1)
        # Initialize count of bad cities
        bad_cities = 0
        
        # Helper function to perform DFS and assign companies
        def dfs(node, parent, current_company):
            nonlocal bad_cities
            company[node] = current_company
            visited.add(node)
            degree = len(adj_list[node]) - (parent != 0)
            if degree > 2:
                bad_cities += 1
            
            for neighbor in adj_list[node]:
                if neighbor == parent:
                    continue
                if company[neighbor] == 0:
                    dfs(neighbor, node, (current_company % r) + 1)
        
        # Try to assign companies starting from each node
        for i in range(1, n + 1):
            if company[i] == 0:
                visited = set()
                dfs(i, 0, 1)
        
        return bad_cities <= k
    
    # Binary search for the minimum number of companies
    left, right = 1, n - 1
    while left < right:
        mid = (left + right) // 2
        if can_partition(mid):
            right = mid
        else:
            left = mid + 1
    
    # Assign companies using the found minimum number of companies
    company = [0] * (n + 1)
    bad_cities = 0
    visited = set()
    
    def dfs_assign(node, parent, current_company):
        nonlocal bad_cities
        company[node] = current_company
        visited.add(node)
        degree = len(adj_list[node]) - (parent != 0)
        if degree > 2:
            bad_cities += 1
        
        for neighbor in adj_list[node]:
            if neighbor == parent:
                continue
            if company[neighbor] == 0:
                dfs_assign(neighbor, node, (current_company % left) + 1)
    
    for i in range(1, n + 1):
        if company[i] == 0:
            dfs_assign(i, 0, 1)
    
    return left, company[1:]

# Main function to handle input and output
def main():
    n, k, roads = read_input()
    r, companies = solve(n, k, roads)
    print(r)
    print(' '.join(map(str, companies)))

if __name__ == "__main__":
    main()