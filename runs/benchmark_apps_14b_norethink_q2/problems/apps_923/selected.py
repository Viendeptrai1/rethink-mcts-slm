import sys

def is_real_puzzle(n, active_teeth):
    # Check if the sequence can be transformed into 0, 1, 2, ..., n-1
    target = list(range(n))
    
    # Try to simulate the button presses
    for _ in range(n):
        # Rotate the gears
        new_active_teeth = []
        for i in range(n):
            if i % 2 == 0:
                # Clockwise rotation
                new_active_teeth.append((active_teeth[i] + 1) % n)
            else:
                # Counter-clockwise rotation
                new_active_teeth.append((active_teeth[i] - 1) % n)
        
        # Check if we have reached the target sequence
        if new_active_teeth == target:
            return "Yes"
        
        # Update the active teeth for the next iteration
        active_teeth = new_active_teeth
    
    return "No"

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    active_teeth = list(map(int, data[1:]))
    
    result = is_real_puzzle(n, active_teeth)
    print(result)

if __name__ == "__main__":
    main()