import sys
import math

def max_gcd_after_replacement(N, A):
    current_gcd = A[0]
    for i in range(1, N):
        current_gcd = math.gcd(current_gcd, A[i])
    
    max_gcd = 0
    prefix_gcd = [0] * N
    suffix_gcd = [0] * N
    
    prefix_gcd[0] = A[0]
    for i in range(1, N):
        prefix_gcd[i] = math.gcd(prefix_gcd[i-1], A[i])
    
    suffix_gcd[N-1] = A[N-1]
    for i in range(N-2, -1, -1):
        suffix_gcd[i] = math.gcd(suffix_gcd[i+1], A[i])
    
    for i in range(N):
        if i == 0:
            new_gcd = suffix_gcd[1]
        elif i == N - 1:
            new_gcd = prefix_gcd[N-2]
        else:
            new_gcd = math.gcd(prefix_gcd[i-1], suffix_gcd[i+1])
        
        max_gcd = max(max_gcd, new_gcd)
    
    return max_gcd

def main():
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    A = list(map(int, data[1:]))
    
    result = max_gcd_after_replacement(N, A)
    print(result)

if __name__ == "__main__":
    main()