MOD = 998244353

def count_distinct_integers(N, X, A):
    from itertools import product
    
    # Convert binary strings to integers
    X = int(X, 2)
    A = [int(A[i], 2) for i in range(N)]
    
    # Set to store all distinct integers on the board
    possible_numbers = set(A)
    
    # Perform operations using dynamic programming
    max_possible = 2 * max(A)
    reachable = [False] * (max_possible + 1)
    
    for num in A:
        reachable[num] = True

    # Double operation
    for num in A:
        doubled = 2 * num
        if doubled <= max_possible:
            reachable[doubled] = True
    
    # XOR operation
    for i in range(max_possible + 1):
        for j in range(max_possible + 1):
            xor_result = i ^ j
            if xor_result <= max_possible:
                reachable[xor_result] = True
    
    # Count how many reachable numbers are <= X
    count = sum(1 for i in range(X + 1) if reachable[i])
    
    return count % MOD

def main():
    import sys
    input = sys.stdin.read
    data = input().strip().split()
    
    N = int(data[0])
    X = data[1]
    A = data[2:]
    
    result = count_distinct_integers(N, X, A)
    print(result)

if __name__ == "__main__":
    main()