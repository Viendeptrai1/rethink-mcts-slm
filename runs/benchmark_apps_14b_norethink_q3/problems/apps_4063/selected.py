import sys
input = sys.stdin.read
data = input().split()

N = int(data[0])
difficulties = list(map(int, data[1:]))

difficulties.sort()

def count_problems(K):
    left_count = sum(1 for d in difficulties if d < K)
    right_count = N - left_count
    return left_count, right_count

left, right = 1, 10**5 + 1
result = 0

while left < right:
    mid = (left + right) // 2
    left_count, right_count = count_problems(mid)
    
    if left_count == right_count:
        result += 1
        # Check if there are more K values that satisfy the condition
        # by moving both pointers inward
        left_mid = mid - 1
        right_mid = mid + 1
        while left_mid >= 1 and count_problems(left_mid)[0] == count_problems(left_mid)[1]:
            result += 1
            left_mid -= 1
        while right_mid <= 10**5 and count_problems(right_mid)[0] == count_problems(right_mid)[1]:
            result += 1
            right_mid += 1
        break
    elif left_count < right_count:
        left = mid + 1
    else:
        right = mid

print(result)