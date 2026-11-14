import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    n = int(input_data[0])
    t = input_data[1]
    
    s = []
    index = 0
    count = 1
    while index < n:
        s.append(t[index])
        index += count
        count += 1
    
    print("".join(s))

if __name__ == "__main__":
    solve()