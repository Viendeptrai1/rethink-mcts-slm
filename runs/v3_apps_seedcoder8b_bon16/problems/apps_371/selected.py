def solve(m):
    def ways_for_n(n):
        count = 0
        for a in range(1, n + 1):
            if a * (a * a + a + 1) <= m:
                count += 1
            else:
                break
        return count
    
    left, right = 1, 10**15
    answer = -1
    while left <= right:
        mid = (left + right) // 2
        if ways_for_n(mid) == m:
            answer = mid
            right = mid - 1
        elif ways_for_n(mid) < m:
            left = mid + 1
        else:
            right = mid - 1
    return answer

import sys
input = sys.stdin.read
m = int(input().strip())
print(solve(m))