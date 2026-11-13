import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    a = int(input_data[0])
    b = int(input_data[1])
    c = int(input_data[2])
    d = int(input_data[3])
    
    # Sort the initial positions
    coords = sorted([a, b, c])
    x, y, z = coords[0], coords[1], coords[2]
    
    # Calculate the cost to fix the distance between the first and second
    # We need y - x >= d. If not, we need to move y to the right by (d - (y - x))
    cost1 = max(0, d - (y - x))
    
    # Calculate the cost to fix the distance between the second and third
    # We need z - y >= d. However, y might have moved to the right.
    # The new position of the middle person would be y + cost1.
    # So we need z - (y + cost1) >= d => z - y - cost1 >= d
    # If not, we need to move z to the right by (d - (z - y - cost1))
    cost2 = max(0, d - (z - y - cost1))
    
    print(cost1 + cost2)

if __name__ == "__main__":
    solve()