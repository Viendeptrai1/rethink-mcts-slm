def is_real_puzzle(n, active_tooth_sequence):
    # We need to check if we can push the button enough times to rearrange the active teeth into 0, 1, 2, ..., n-1
    # Create a list of tuples where each tuple represents the gear's index and its active tooth value
    gears = list(enumerate(active_tooth_sequence))

    for _ in range(n):  # Try up to n rotations as the number of pushes
        # Simulate the rotation for each gear
        new_gears = [0] * n
        for i in range(n):
            if i % 2 == 0:
                # Clockwise rotation
                new_gears[i] = (gears[i][1] + 1) % n
            else:
                # Counter-clockwise rotation
                new_gears[i] = (gears[i][1] - 1) % n
        
        # Update the gears with new active teeth positions
        gears = [(i, new_gears[i]) for i in range(n)]
        
        # Check if the active teeth form the sequence 0, 1, 2, ..., n-1
        if [active_tooth for _, active_tooth in gears] == list(range(n)):
            return "Yes"
    
    return "No"

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    active_tooth_sequence = list(map(int, data[1:]))
    
    result = is_real_puzzle(n, active_tooth_sequence)
    print(result)