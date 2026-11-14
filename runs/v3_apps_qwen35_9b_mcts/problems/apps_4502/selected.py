import sys
from collections import deque

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    n = int(input_data[0])
    a = [int(x) for x in input_data[1:]]
    
    b = deque()
    # direction: True means we append to the right (end), False means we append to the left (front)
    # Initially, after appending a_1, we reverse, so the next append should go to the front relative to current logical order
    # Let's simulate carefully:
    # Step 1: append a1 -> [a1], then reverse -> [a1] (same)
    # Step 2: append a2 -> [a1, a2], then reverse -> [a2, a1]
    # Step 3: append a3 -> [a2, a1, a3], then reverse -> [a3, a1, a2]
    # Step 4: append a4 -> [a3, a1, a2, a4], then reverse -> [a4, a2, a1, a3]
    
    # Pattern observation:
    # We can maintain a deque and a direction flag.
    # If direction is 1 (normal), we append to the right. Then we conceptually reverse, which means next append goes to left.
    # If direction is -1 (reversed), we append to the left. Then we conceptually reverse, which means next append goes to right.
    # Actually, let's track the logical state without physically reversing.
    # Let 'dir' be 1 if the current deque represents the sequence in normal order, -1 if reversed.
    # Operation i:
    #   If dir == 1:
    #     Append a_i to the right end of deque.
    #     Then reverse the logical meaning: dir becomes -1.
    #   If dir == -1:
    #     Append a_i to the left end of deque.
    #     Then reverse the logical meaning: dir becomes 1.
    #
    # Initial state: empty deque, dir = 1.
    # i=1: dir=1 -> append a1 to right -> [a1], dir becomes -1.
    # i=2: dir=-1 -> append a2 to left -> [a2, a1], dir becomes 1.
    # i=3: dir=1 -> append a3 to right -> [a2, a1, a3], dir becomes -1.
    # i=4: dir=-1 -> append a4 to left -> [a4, a2, a1, a3], dir becomes 1.
    # Final result: if dir is 1, print left to right. If dir is -1, print right to left.
    
    dir_flag = 1
    for x in a:
        if dir_flag == 1:
            b.append(x)
            dir_flag = -1
        else:
            b.appendleft(x)
            dir_flag = 1
            
    if dir_flag == 1:
        print(" ".join(map(str, b)))
    else:
        print(" ".join(map(str, reversed(b))))

if __name__ == '__main__':
    solve()