import sys

def min_lights_to_turn_off(n, lights):
    k = 0
    i = 1
    while i < n - 1:
        if lights[i - 1] == 1 and lights[i] == 0 and lights[i + 1] == 1:
            # Found a disturbance at position i
            k += 1
            # Skip the next two positions as they are affected
            i += 3
        else:
            i += 1
    return k

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    lights = list(map(int, data[1:]))
    
    result = min_lights_to_turn_off(n, lights)
    print(result)