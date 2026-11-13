import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    n = int(input_data[0])
    a = [int(x) for x in input_data[1:]]
    
    # Count consecutive 1s in the original array
    max_rest = 0
    current_rest = 0
    for x in a:
        if x == 1:
            current_rest += 1
            max_rest = max(max_rest, current_rest)
        else:
            current_rest = 0
    
    # If there is at least one 0 (guaranteed), we need to check the wrap-around case
    # The wrap-around rest is formed by the suffix of 1s at the end + prefix of 1s at the start
    if max_rest == 0:
        # No 1s at all
        print(0)
        return
    
    # Count suffix 1s
    suffix_ones = 0
    for i in range(n-1, -1, -1):
        if a[i] == 1:
            suffix_ones += 1
        else:
            break
    
    # Count prefix 1s
    prefix_ones = 0
    for i in range(n):
        if a[i] == 1:
            prefix_ones += 1
        else:
            break
    
    # The wrap-around rest length is suffix_ones + prefix_ones
    # However, we must ensure we don't double count if the whole array is 1s, 
    # but the problem guarantees at least one 0, so this is safe.
    wrap_around = suffix_ones + prefix_ones
    
    print(max(max_rest, wrap_around))

if __name__ == "__main__":
    solve()