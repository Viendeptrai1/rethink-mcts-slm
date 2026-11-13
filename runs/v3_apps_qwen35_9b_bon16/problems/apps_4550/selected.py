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
    
    target = total // 2
    
    # Check if any single pack equals target
    if a == target or b == target or c == target:
        print("Yes")
        return
    
    # Check if sum of any two packs equals target
    if a + b == target or a + c == target or b + c == target:
        print("Yes")
        return
    
    print("No")

if __name__ == "__main__":
    solve()