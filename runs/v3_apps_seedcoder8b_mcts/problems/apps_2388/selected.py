MOD = 998244353

def count_remaining_robot_sets(N, positions, distances):
    from collections import defaultdict
    import sys
    sys.setrecursionlimit(10**6)

    # Sort robots by their starting position
    robots = sorted(zip(positions, distances))

    # Create a graph where each robot points to the robots it can activate
    graph = defaultdict(list)
    for i, (x_i, d_i) in enumerate(robots):
        for j, (x_j, d_j) in enumerate(robots):
            if i != j and x_i <= x_j < x_i + d_i:
                graph[i].append(j)

    # Memoization dictionary to store results of subproblems
    memo = {}

    def dfs(mask):
        if mask in memo:
            return memo[mask]

        # Count the number of robots that are still active
        active_count = bin(mask).count('1')

        # If no robots are active, there's only one way (the empty set)
        if active_count == 0:
            return 1

        # Try activating each robot and see the resulting sets
        result = 0
        for i in range(N):
            if mask & (1 << i):
                # Activate robot i
                new_mask = mask
                for j in graph[i]:
                    if new_mask & (1 << j):
                        new_mask ^= (1 << j)
                new_mask ^= (1 << i)
                result = (result + dfs(new_mask)) % MOD

        memo[mask] = result
        return result

    # Start with all robots active
    full_mask = (1 << N) - 1
    return dfs(full_mask)

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    positions = []
    distances = []
    
    index = 1
    for _ in range(N):
        positions.append(int(data[index]))
        distances.append(int(data[index + 1]))
        index += 2
    
    result = count_remaining_robot_sets(N, positions, distances)
    print(result)

if __name__ == "__main__":
    main()