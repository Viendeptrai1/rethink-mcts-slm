from sys import stdin, stdout
import math

MOD = 998244353

def mod_inv(a):
    return pow(a, MOD - 2, MOD)

def main():
    input = stdin.read
    data = input().split()
    
    n = int(data[0])
    m = int(data[1])
    a = list(map(int, data[2:n+2]))
    w = list(map(int, data[n+2:2*n+2]))
    
    total_weight = sum(w)
    like_count = sum(a)
    dislike_count = n - like_count
    
    like_weight_sum = sum(w[i] * (1 + a[i]) for i in range(n))
    dislike_weight_sum = sum(w[i] * (1 - a[i]) for i in range(n))
    
    like_expected = (like_weight_sum * like_count + dislike_weight_sum * dislike_count) % MOD
    dislike_expected = (dislike_weight_sum * like_count + like_weight_sum * dislike_count) % MOD
    
    like_result = (like_expected * mod_inv(like_count)) % MOD
    dislike_result = (dislike_expected * mod_inv(dislike_count)) % MOD
    
    result = [like_result if a[i] == 1 else dislike_result for i in range(n)]
    
    for num in result:
        stdout.write(f"{num}\n")

if __name__ == "__main__":
    main()