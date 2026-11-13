import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    a = list(map(int, data[1:]))
    
    # Check if the sequence can be split into one increasing and one decreasing
    def can_split(a):
        if len(a) <= 1:
            return True
        
        increasing = False
        decreasing = False
        
        i = 1
        while i < len(a) and a[i] >= a[i - 1]:
            i += 1
            increasing = True
        
        j = i - 1
        while j < len(a) - 1 and a[j] >= a[j + 1]:
            j += 1
            decreasing = True
        
        return increasing and decreasing and j == i - 1
    
    if not can_split(a):
        print("NO")
        return
    
    # Split the sequence into increasing and decreasing parts
    inc_end = -1
    dec_start = -1
    
    for i in range(1, n):
        if a[i] >= a[i - 1]:
            inc_end = i
    
    for i in range(n - 2, -1, -1):
        if a[i] >= a[i + 1]:
            dec_start = i
            break
    
    # Create the result array
    res = [0] * n
    for i in range(inc_end + 1):
        res[i] = 0
    
    for i in range(dec_start, n):
        res[i] = 1
    
    print("YES")
    print(' '.join(map(str, res)))

if __name__ == "__main__":
    solve()