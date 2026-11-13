import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    n = int(input_data[0])
    a = [int(x) for x in input_data[1:n+1]]
    
    # We need to find if there exists a non-negative integer k (number of button pushes)
    # such that after k pushes, the active teeth become 0, 1, 2, ..., n-1.
    
    # Let's analyze the movement for the i-th gear (0-indexed in code, 1-indexed in problem):
    # The problem states:
    # Gear 1 (index 0): rotates clockwise.
    # Gear 2 (index 1): rotates counter-clockwise.
    # Gear 3 (index 2): rotates clockwise.
    # ...
    # Gear i (index i-1): rotates clockwise if (i-1) is even, counter-clockwise if (i-1) is odd.
    
    # The teeth are numbered 0 to n-1 in counter-clockwise order.
    # Clockwise rotation: the active tooth moves to the next number in the sequence (0 -> 1 -> 2 ...).
    # Counter-clockwise rotation: the active tooth moves to the previous number (0 -> n-1 -> n-2 ...).
    
    # Let current active tooth of gear i be a[i].
    # Target active tooth for gear i is i (since we want sequence 0, 1, 2, ..., n-1).
    
    # For gear i (0-indexed):
    # If i is even (0, 2, 4...): rotates clockwise.
    #   Each push adds 1 to the value modulo n.
    #   Equation: (a[i] + k) % n = i
    #   => k % n = (i - a[i]) % n
    # If i is odd (1, 3, 5...): rotates counter-clockwise.
    #   Each push subtracts 1 from the value modulo n.
    #   Equation: (a[i] - k) % n = i
    #   => -k % n = (i - a[i]) % n
    #   => k % n = (a[i] - i) % n
    
    # So for each gear i, we can calculate the required remainder of k modulo n.
    # If all gears require the same remainder, then a solution exists.
    
    required_remainder = -1
    
    possible = True
    for i in range(n):
        target = i
        current = a[i]
        
        if i % 2 == 0:
            # Clockwise: (current + k) % n = target
            # k % n = (target - current) % n
            rem = (target - current) % n
        else:
            # Counter-clockwise: (current - k) % n = target
            # -k % n = (target - current) % n
            # k % n = (current - target) % n
            rem = (current - target) % n
        
        if required_remainder == -1:
            required_remainder = rem
        elif required_remainder != rem:
            possible = False
            break
    
    if possible:
        print("Yes")
    else:
        print("No")

if __name__ == "__main__":
    solve()