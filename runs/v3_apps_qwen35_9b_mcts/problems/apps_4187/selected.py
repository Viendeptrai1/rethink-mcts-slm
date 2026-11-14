import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    n = int(input_data[0])
    a = [int(x) for x in input_data[1:1+n]]

    # If there are no rest hours at all, the answer is 0
    if 1 not in a:
        print(0)
        return

    # Calculate max consecutive 1s in a single day
    max_rest = 0
    current_rest = 0
    for x in a:
        if x == 1:
            current_rest += 1
            if current_rest > max_rest:
                max_rest = current_rest
        else:
            current_rest = 0

    # Calculate wrap-around rest: suffix of 1s + prefix of 1s
    suffix_rest = 0
    for i in range(n-1, -1, -1):
        if a[i] == 1:
            suffix_rest += 1
        else:
            break

    prefix_rest = 0
    for i in range(n):
        if a[i] == 1:
            prefix_rest += 1
        else:
            break

    wrap_rest = suffix_rest + prefix_rest
    # The wrap-around rest cannot exceed the total number of 1s in the array,
    # but since we are looking for continuous hours across days, 
    # the sequence effectively repeats, so the max continuous block 
    # involving wrap-around is simply suffix + prefix.
    # However, we must ensure we don't count a full cycle if the whole array is 1s,
    # but the problem guarantees at least one 0, so suffix+prefix < n always.
    
    print(max(max_rest, wrap_rest))

if __name__ == "__main__":
    solve()