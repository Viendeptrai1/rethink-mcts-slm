import sys

def min_flats_to_turn_off(n, a):
    k = 0
    for i in range(1, n - 1):
        if a[i - 1] == a[i + 1] == 1 and a[i] == 0:
            k += 1
            a[i] = 1  # Turn on the light to simulate turning off the disturbance
    return k

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    a = list(map(int, data[1:]))
    
    result = min_flats_to_turn_off(n, a)
    print(result)