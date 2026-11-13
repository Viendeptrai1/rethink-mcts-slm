def count_ways_to_climb(N, M, broken_steps):
    MOD = 1_000_000_007

    # Initialize a list to store the number of ways to reach each step
    ways = [0] * (N + 1)
    # Start point
    ways[0] = 1

    # Create a set of broken steps for quick access
    broken_set = set(broken_steps)

    for step in range(1, N + 1):
        if step not in broken_set:
            # If the step is not broken, accumulate the number of ways to reach here
            ways[step] = ways[step - 1]
            if step > 1:
                ways[step] = (ways[step] + ways[step - 2]) % MOD

    return ways[N]

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    # First line contains N and M
    N = int(data[0])
    M = int(data[1])
    
    # The next M lines contain the broken steps
    broken_steps = list(map(int, data[2:2 + M]))
    
    # Calculate the number of ways to climb the stairs
    result = count_ways_to_climb(N, M, broken_steps)
    
    # Print the result
    print(result)

if __name__ == "__main__":
    main()