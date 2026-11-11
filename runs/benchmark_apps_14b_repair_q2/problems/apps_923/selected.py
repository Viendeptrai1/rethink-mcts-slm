import sys

def is_real_puzzle(n, active_teeth):
    # Check if the sequence can be transformed into 0, 1, 2, ..., n-1
    target = list(range(n))
    current = active_teeth[:]
    
    # Try to match the target sequence by rotating the gears
    for _ in range(n):
        if current == target:
            return "Yes"
        
        # Rotate the gears
        for i in range(n):
            if i % 2 == 0:
                # Clockwise rotation
                current[i] = (current[i] + 1) % n
            else:
                # Counter-clockwise rotation
                current[i] = (current[i] - 1) % n
    
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