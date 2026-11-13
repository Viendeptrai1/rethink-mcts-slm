def min_instability(n, a):
    prefix_max = [a[0]]
    prefix_min = [a[0]]
    suffix_max = [a[-1]]
    suffix_min = [a[-1]]

    for i in range(1, n):
        prefix_max.append(max(prefix_max[-1], a[i]))
        prefix_min.append(min(prefix_min[-1], a[i]))

    for i in range(n-2, -1, -1):
        suffix_max.append(max(suffix_max[-1], a[i]))
        suffix_min.append(min(suffix_min[-1], a[i]))

    suffix_max.reverse()
    suffix_min.reverse()

    min_instab = float('inf')
    for i in range(n):
        left_max = prefix_max[i-1] if i > 0 else float('-inf')
        left_min = prefix_min[i-1] if i > 0 else float('inf')
        right_max = suffix_max[i+1] if i < n-1 else float('-inf')
        right_min = suffix_min[i+1] if i < n-1 else float('inf')

        instab = max(left_max, right_max) - min(left_min, right_min)
        min_instab = min(min_instab, instab)

    return min_instab

# Example usage:
import sys
input = sys.stdin.read
data = input().split()
n = int(data[0])
a = list(map(int, data[1:]))

print(min_instability(n, a))