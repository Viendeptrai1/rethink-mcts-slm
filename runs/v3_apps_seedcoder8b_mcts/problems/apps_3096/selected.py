import sys
from collections import defaultdict, deque

def count_joke_sets(N, jokes, supervisors):
    # Build the tree structure
    tree = defaultdict(list)
    for a, b in supervisors:
        tree[b].append(a)
    
    # Dynamic programming table
    dp = [0] * (N + 1)
    
    # Sort jokes and keep track of original indices
    sorted_jokes = sorted((joke, i + 1) for i, joke in enumerate(jokes))
    
    # Initialize the dp array for leaf nodes
    for i in range(1, N + 1):
        if not tree[i]:
            dp[i] = 1
    
    # Process nodes in topological order
    queue = deque([1])
    while queue:
        node = queue.popleft()
        for child in tree[node]:
            queue.append(child)
            # Check if the child can be invited
            if all(dp[superior] for superior in tree[child]):
                # Check for consecutive joke types
                child_joke = jokes[child - 1]
                if all(abs(child_joke - joke) == 1 for joke, _ in sorted_jokes if _ != child):
                    dp[child] = 1
    
    # Count valid sets
    return sum(dp[1:])

def main():
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    jokes = list(map(int, data[1:N+1]))
    supervisors = [(int(data[i]), int(data[i+1])) for i in range(N, len(data), 2)]
    
    result = count_joke_sets(N, jokes, supervisors)
    print(result)

if __name__ == "__main__":
    main()