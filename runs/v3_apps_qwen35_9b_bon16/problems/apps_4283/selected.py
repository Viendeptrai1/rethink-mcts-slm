import sys

def solve():
    data = sys.stdin.read().split()
    if not data:
        return
    n = int(data[0])
    a = [int(x) for x in data[1:]]
    
    a.sort()
    left = 0
    max_len = 0
    
    for right in range(n):
        while a[right] - a[left] > 5:
            left += 1
        current_len = right - left + 1
        if current_len > max_len:
            max_len = current_len
            
    print(max_len)

if __name__ == "__main__":
    solve()