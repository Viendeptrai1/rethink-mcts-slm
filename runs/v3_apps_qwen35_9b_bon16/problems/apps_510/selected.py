import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    a = int(input_data[0])
    b = int(input_data[1])
    c = int(input_data[2])
    d = int(input_data[3])

    coords = [a, b, c]
    coords.sort()
    
    # Distance between first and second must be at least d
    # If coords[1] - coords[0] < d, we need to move coords[0] left by (d - diff)
    move1 = 0
    if coords[1] - coords[0] < d:
        move1 = d - (coords[1] - coords[0])
    
    # Distance between second and third must be at least d
    # If coords[2] - coords[1] < d, we need to move coords[2] right by (d - diff)
    move2 = 0
    if coords[2] - coords[1] < d:
        move2 = d - (coords[2] - coords[1])
    
    print(move1 + move2)

if __name__ == "__main__":
    solve()