from typing import List
import sys

def count_valid_k(N: int, difficulties: List[int]) -> int:
    difficulties.sort()
    mid = N // 2
    left_sum = sum(difficulties[:mid])
    right_sum = sum(difficulties[mid:])
    count = 0
    if left_sum == right_sum:
        count += 1
    for i in range(mid, N):
        left_sum += difficulties[i] - difficulties[i - mid]
        right_sum -= difficulties[i] - difficulties[i - mid]
        if left_sum == right_sum:
            count += 1
    return count

if __name__ == "__main__":
    input = sys.stdin.read
    data = input().split()
    N = int(data[0])
    difficulties = list(map(int, data[1:]))
    result = count_valid_k(N, difficulties)
    print(result)