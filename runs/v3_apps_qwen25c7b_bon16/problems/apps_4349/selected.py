from collections import defaultdict, deque

def min_day_to_play(n, m, k, offers):
    # Create a graph to represent the days when microtransactions are on sale
    graph = defaultdict(list)
    for d, t in offers:
        graph[d].append(t - 1)  # Adjust index to be 0-based

    # Initialize variables
    max_day = max(offers, key=lambda x: x[0])[0]
    dp = [float('inf')] * n
    visited = set()
    queue = deque()

    # Process each day starting from day 1 to max_day
    for day in range(1, max_day + 1):
        # Add new offers to the queue
        while queue and queue[0] < day:
            queue.popleft()

        # Update dp array with current day's offers
        for t in graph[day]:
            if t not in visited:
                dp[t] = min(dp[t], dp[t] if dp[t] != float('inf') else 1, dp[(t - 1) % n] + 1 if (t - 1) % n != float('inf') else 2)
                visited.add(t)
                queue.append(day + 1)

        # Check if we have all microtransactions ordered by day
        if all(dp[i] <= k[i] for i in range(n)):
            return day

# Example usage:
if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    m = int(data[1])
    k = list(map(int, data[2:2+n]))
    offers = [(int(data[2+n+2*i]) - 1, int(data[2+n+2*i+1])) for i in range(m)]
    
    result = min_day_to_play(n, m, k, offers)
    print(result)