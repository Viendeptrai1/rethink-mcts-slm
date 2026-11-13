import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    
    if not data:
        return
    
    n = int(data[0])
    a = [int(x) for x in data[1:]]
    
    seen = set()
    count = 0
    
    for x in a:
        if x in seen:
            seen.remove(x)
        else:
            seen.add(x)
    
    print(len(seen))

if __name__ == "__main__":
    solve()