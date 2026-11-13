import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    n = int(input_data[0])
    t = input_data[1]
    
    s = []
    index = 0
    for i in range(1, n + 1):
        s.append(t[index])
        index += i
    
    print("".join(s))

if __name__ == "__main__":
    solve()