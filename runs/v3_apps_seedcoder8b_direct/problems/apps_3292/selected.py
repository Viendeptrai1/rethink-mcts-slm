def count_possible_rankings(n, names):
    MOD = 1_000_000_007

    # Sort names lexicographically
    names.sort()

    # Create a list to store the number of valid orderings for each prefix
    dp = [1] * n

    # Iterate over each name
    for i in range(1, n):
        # Compare the current name with the previous one
        if names[i].startswith(names[i - 1]):
            # If they share the same prefix, they can be placed together
            dp[i] = dp[i - 1]
        else:
            # Otherwise, calculate the number of valid orderings
            # by considering all previous valid orderings
            dp[i] = sum(dp[:i]) % MOD

    # The result is the sum of all valid orderings
    return sum(dp) % MOD

def main():
    import sys
    input = sys.stdin.read
    data = input().splitlines()
    
    n = int(data[0])
    names = data[1:n+1]
    
    result = count_possible_rankings(n, names)
    print(result)

if __name__ == "__main__":
    main()