import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    n = int(input_data[0])
    p = [int(x) for x in input_data[1:]]
    
    if n == 0:
        print(0)
        return
    
    # Create a position map: value -> index
    pos = [0] * (n + 1)
    for i in range(n):
        pos[p[i]] = i
    
    # Find the longest contiguous subsegment of values [x, x+1, ..., y]
    # such that they appear in the array in increasing order of their indices.
    # That is, pos[x] < pos[x+1] < ... < pos[y].
    
    max_len = 1
    current_len = 1
    
    for v in range(2, n + 1):
        if pos[v] > pos[v - 1]:
            current_len += 1
        else:
            if current_len > max_len:
                max_len = current_len
            current_len = 1
    
    if current_len > max_len:
        max_len = current_len
    
    # The minimum number of moves is n - max_len
    print(n - max_len)

if __name__ == "__main__":
    solve()