import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    a = int(input_data[0])
    b = int(input_data[1])
    c = int(input_data[2])
    
    total = a + b + c
    if total % 2 != 0:
        print("No")
        return
    
    half = total // 2
    
    if a == half or b == half or c == half:
        print("Yes")
    elif a + b == half or a + c == half or b + c == half:
        print("Yes")
    else:
        print("No")

if __name__ == "__main__":
    solve()