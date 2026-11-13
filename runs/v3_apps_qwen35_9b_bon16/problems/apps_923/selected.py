import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    n = int(input_data[0])
    a = [int(input_data[i + 1]) for i in range(n)]
    
    # Calculate how many times we need to push the button for each gear
    # to reach the target state (0, 1, 2, ..., n-1)
    # Gear i (0-indexed) target value is i.
    # Current value is a[i].
    
    # For even-indexed gears (0, 2, 4...): rotation is clockwise.
    # Clockwise: 0 -> 1 -> 2 ...
    # To go from a[i] to i clockwise, we need (i - a[i]) mod n steps.
    # Since we want positive steps: (i - a[i] + n) % n
    
    # For odd-indexed gears (1, 3, 5...): rotation is counter-clockwise.
    # Counter-clockwise: 0 -> 4 -> 3 ... (for n=5)
    # Effectively, the value decreases by 1 each step modulo n.
    # To go from a[i] to i counter-clockwise, we need (a[i] - i) mod n steps.
    # Formula: (a[i] - i + n) % n
    
    # Let's verify the logic with Example 1: n=3, a=[1, 0, 0]
    # Target: [0, 1, 2]
    # i=0 (even): target 0, current 1. Steps = (0-1+3)%3 = 2.
    # i=1 (odd): target 1, current 0. Steps = (0-1+3)%3 = 2.
    # i=2 (even): target 2, current 0. Steps = (2-0+3)%3 = 2.
    # All steps are 2. Consistent. So "Yes".
    
    # Example 2: n=5, a=[4, 2, 1, 4, 3]
    # Target: [0, 1, 2, 3, 4]
    # i=0 (even): target 0, cur 4. Steps = (0-4+5)%5 = 1.
    # i=1 (odd): target 1, cur 2. Steps = (2-1+5)%5 = 1.
    # i=2 (even): target 2, cur 1. Steps = (2-1+5)%5 = 1.
    # i=3 (odd): target 3, cur 4. Steps = (4-3+5)%5 = 1.
    # i=4 (even): target 4, cur 3. Steps = (4-3+5)%5 = 1.
    # All steps are 1. Consistent. So "Yes".
    
    # Example 3: n=4, a=[0, 2, 3, 1]
    # Target: [0, 1, 2, 3]
    # i=0 (even): target 0, cur 0. Steps = 0.
    # i=1 (odd): target 1, cur 2. Steps = (2-1+4)%4 = 1.
    # i=2 (even): target 2, cur 3. Steps = (2-3+4)%4 = 3.
    # i=3 (odd): target 3, cur 1. Steps = (1-3+4)%4 = 2.
    # Steps: 0, 1, 3, 2. Not consistent. So "No".
    
    steps = []
    for i in range(n):
        if i % 2 == 0:
            # Even index: clockwise
            s = (i - a[i] + n) % n
        else:
            # Odd index: counter-clockwise
            s = (a[i] - i + n) % n
        steps.append(s)
    
    # Check if all gears require the same number of pushes
    if len(set(steps)) == 1:
        print("Yes")
    else:
        print("No")

if __name__ == "__main__":
    solve()