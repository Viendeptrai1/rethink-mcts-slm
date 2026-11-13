def min_i_to_reach_k(n, k, A):
    current_sum = 0
    for i in range(n):
        current_sum += A[i]
        if current_sum >= k:
            return 0
    A_next = [current_sum]
    i = 1
    while True:
        new_A_next = []
        current_sum = 0
        for j in range(len(A_next)):
            current_sum += A_next[j] - 1
            new_A_next.append(current_sum)
            if current_sum >= k:
                return i
        A_next = new_A_next
        i += 1

# Example usage:
import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])
k = int(data[1])
A = list(map(int, data[2:]))

result = min_i_to_reach_k(n, k, A)
print(result)