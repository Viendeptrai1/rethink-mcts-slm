def solve():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    MOD = 998244353
    
    n = int(data[0])
    m = int(data[1])
    
    a = list(map(int, data[2:n+2]))
    w = list(map(int, data[n+2:2*n+2]))
    
    # Calculate the total weight
    total_weight = sum(w)
    
    # Calculate the expected weight for each picture
    expected_weights = []
    
    for i in range(n):
        if a[i] == 1:
            # Nauuo likes the picture
            w[i] += m
        else:
            # Nauuo does not like the picture
            w[i] -= m
        
        # Calculate the probability of this picture being displayed
        probability = w[i] / total_weight
        
        # Calculate the expected weight
        expected_weight = probability * w[i]
        
        # Convert the expected weight to the required form
        # We need to find r such that r * w[i] ≡ expected_weight (mod MOD)
        # Since expected_weight is an integer, we can use Fermat's Little Theorem
        # r = expected_weight * (w[i]^(MOD-2)) % MOD
        r = (expected_weight * pow(w[i], MOD-2, MOD)) % MOD
        
        expected_weights.append(r)
    
    # Print the results
    print(" ".join(map(str, expected_weights)))