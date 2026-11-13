MOD = 998244353

def mod_inverse(a):
    return pow(a, MOD - 2, MOD)

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    m = int(data[1])
    a = list(map(int, data[2:n+2]))
    w = list(map(int, data[n+2:]))
    
    total_weight = sum(w)
    liked_indices = [i for i in range(n) if a[i] == 1]
    disliked_indices = [i for i in range(n) if a[i] == 0]
    
    for _ in range(m):
        if len(liked_indices) > 0:
            idx = liked_indices.pop()
            w[idx] += 1
            total_weight += 1
            liked_indices.append(idx)
        else:
            idx = disliked_indices.pop()
            w[idx] -= 1
            total_weight -= 1
            disliked_indices.append(idx)
    
    result = []
    for wi in w:
        numerator = (wi * total_weight + MOD) % MOD
        denominator = total_weight
        inverse_denominator = mod_inverse(denominator)
        numerator *= inverse_denominator
        result.append(numerator % MOD)
    
    print(" ".join(map(str, result)))

if __name__ == "__main__":
    main()