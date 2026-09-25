import sys
from sortedcontainers import SortedList

def count_median_pairs(n, m, a):
    count = 0
    prefix_count = [0] * (2 * 10**5 + 1)
    prefix_count[a[0]] = 1
    sl = SortedList([a[0]])
    
    for i in range(1, n):
        prefix_count[a[i]] += 1
        sl.add(a[i])
        
        # Find the number of valid subarrays ending at index i
        left_count = prefix_count[m - 1]
        right_count = prefix_count[m]
        
        if len(sl) % 2 == 1:
            # Odd length subarray
            median_index = len(sl) // 2
            if sl[median_index] == m:
                count += left_count * (right_count + 1)
        else:
            # Even length subarray
            median_index = len(sl) // 2
            if sl[median_index] == m:
                count += left_count * right_count
    
    return count

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    m = int(data[1])
    a = list(map(int, data[2:]))
    
    result = count_median_pairs(n, m, a)
    print(result)

if __name__ == "__main__":
    main()