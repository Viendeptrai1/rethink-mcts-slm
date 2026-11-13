import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return

    n = int(input_data[0])
    a = list(map(int, input_data[1:1+n]))

    if n == 1:
        print(-1)
        return

    # The cycle is: 0, 1, 2, ..., 14, 15, 14, ..., 1, 0
    # Length is 30.
    # We can try to match the given sequence against the cycle starting at different offsets.
    # Since the input is guaranteed to be consistent, there should be at most one valid position
    # in the cycle that matches the sequence, or possibly two if the sequence is short and symmetric.
    
    cycle = list(range(16)) + list(range(14, 0, -1))
    
    # Try to find all starting positions in the cycle that match the input sequence
    valid_starts = []
    for start in range(30):
        match = True
        for i in range(n):
            if a[i] != cycle[(start + i) % 30]:
                match = False
                break
        if match:
            valid_starts.append(start)
    
    # If we have multiple valid starts, we need to check if they lead to the same next value.
    # The next value corresponds to index (start + n) % 30.
    # We look at the value at that index for each valid start.
    
    next_values = []
    for start in valid_starts:
        next_val = cycle[(start + n) % 30]
        next_values.append(next_val)
    
    if len(set(next_values)) == 1:
        val = next_values[0]
        if val < a[-1]:
            print("DOWN")
        else:
            print("UP")
    else:
        print(-1)

if __name__ == "__main__":
    solve()