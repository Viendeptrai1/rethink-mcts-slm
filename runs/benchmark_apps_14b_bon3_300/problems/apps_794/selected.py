import sys

def solve():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    a = list(map(int, data[1:]))
    
    total_sum = sum(a)
    if total_sum % 2 != 0:
        print("-1")
        return
    
    target_sum = total_sum // 2
    
    a.sort(reverse=True)
    
    left_sum = 0
    right_sum = 0
    left_part = []
    right_part = []
    
    for num in a:
        if left_sum <= right_sum:
            left_part.append(num)
            left_sum += num
        else:
            right_part.append(num)
            right_sum += num
    
    if left_sum == right_sum:
        print("-1")
    else:
        result = left_part + right_part
        print(" ".join(map(str, result)))

if __name__ == "__main__":
    solve()