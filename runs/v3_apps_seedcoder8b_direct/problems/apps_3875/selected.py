def expected_longest_increasing_subsequence():
    import sys
    input = sys.stdin.read
    MOD = 1000000007

    def mod_inv(a, p):
        return pow(a, p - 2, p)

    data = input().strip().split()
    N = int(data[0])
    A = list(map(int, data[1:]))

    # Calculate the total number of sequences
    total_sequences = 1
    for a in A:
        total_sequences *= a
        total_sequences %= MOD

    # Calculate the expected value of the length of the longest increasing subsequence
    expected_value = 0
    for a in A:
        # For each A_i, the probability of having a longest increasing subsequence of length i is:
        # (a choose i) / a^N
        # We need to sum this for i from 1 to a
        for i in range(1, a + 1):
            # Calculate (a choose i) % MOD
            choose = 1
            for j in range(i):
                choose = choose * (a - j) % MOD
                choose = choose * mod_inv(j + 1, MOD) % MOD
            
            # Add the contribution to the expected value
            contribution = choose * mod_inv(a, MOD) % MOD
            expected_value = (expected_value + contribution) % MOD

    # Multiply by the total number of sequences and take modulo
    expected_value = expected_value * mod_inv(total_sequences, MOD) % MOD

    print(expected_value)