def solve():
    import math
    from collections import deque

    n = int(input())
    hills = list(map(int, input().split()))

    def is_peak(i):
        return (i == 0 or hills[i] > hills[i-1]) and (i == n-1 or hills[i] > hills[i+1])

    def count_peaks():
        return sum(1 for i in range(n) if is_peak(i))

    def min_time_for_k(k):
        queue = deque()
        for i in range(n):
            if not is_peak(i):
                queue.append((hills[i], i))
        
        peaks_needed = k - count_peaks()
        if peaks_needed <= 0:
            return 0

        time = 0
        while queue and peaks_needed > 0:
            height, index = queue.popleft()
            new_height = max(0, height - 1)
            hills[index] = new_height
            time += height - new_height
            if new_height > 0 and not is_peak(index):
                queue.append((new_height, index))
            peaks_needed -= 1

        return time if peaks_needed == 0 else -1

    max_k = math.ceil(n / 2)
    result = [min_time_for_k(k) for k in range(1, max_k + 1)]
    print(*result)

solve()