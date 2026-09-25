import sys
from bisect import bisect_left

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    a = list(map(int, data[1:]))
    
    total_sum = sum(a)
    nice_indices = []
    
    for i in range(n):
        remaining_sum = total_sum - a[i]
        if remaining_sum % 2 == 0:
            target = remaining_sum // 2
            if target in a and (target != a[i] or a.count(target) > 1):
                nice_indices.append(i + 1)
    
    print(len(nice_indices))
    if nice_indices:
        print(" ".join(map(str, nice_indices)))

if __name__ == "__main__":
    main()