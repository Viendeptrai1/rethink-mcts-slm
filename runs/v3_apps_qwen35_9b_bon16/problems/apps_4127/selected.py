import sys

def solve():
    line = sys.stdin.read().strip()
    if not line:
        return
    parts = line.split()
    A = int(parts[0])
    B_str = parts[1]
    
    # Parse B as integer representing cents to avoid floating point issues
    # B has two digits after decimal, so multiply by 100 and parse as int
    if '.' in B_str:
        integer_part, decimal_part = B_str.split('.')
        decimal_part = decimal_part.ljust(2, '0')[:2]
        B_cents = int(integer_part) * 100 + int(decimal_part)
    else:
        B_cents = int(B_str) * 100
    
    # Compute floor(A * B)
    # Since B is given with two decimal places, A * B = (A * B_cents) / 100
    # We need floor of this value, which is (A * B_cents) // 100
    result = (A * B_cents) // 100
    print(result)

if __name__ == "__main__":
    solve()