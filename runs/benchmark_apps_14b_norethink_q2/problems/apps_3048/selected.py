import sys
from collections import defaultdict

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    edges = [(int(data[2*i+1]), int(data[2*i+2])) for i in range(N-1)]
    
    # Create adjacency list
    adj_list = defaultdict(list)
    for u, v in edges:
        adj_list[u].append(v)
        adj_list[v].append(u)
    
    # Calculate the degree of each node
    degrees = [len(adj_list[i]) for i in range(1, N+1)]
    
    # Calculate the number of optimal paths of length 2
    result = 0
    for degree in degrees:
        if degree >= 2:
            result += degree * (degree - 1)
    
    print(result)

if __name__ == "__main__":
    main()