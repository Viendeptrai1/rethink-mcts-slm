def alice_minus_bob_score(N, a):
    a.sort(reverse=True)
    return sum(a[::2]) - sum(a[1::2])

# Example usage:
import sys
input = sys.stdin.read
data = input().split()
N = int(data[0])
a = list(map(int, data[1:]))

result = alice_minus_bob_score(N, a)
print(result)