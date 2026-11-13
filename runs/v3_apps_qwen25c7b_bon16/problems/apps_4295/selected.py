import sys
input = sys.stdin.read
data = input().split()

N = int(data[0])
K = int(data[1])

result = min(N % K, (K - N % K) % K)
print(result)