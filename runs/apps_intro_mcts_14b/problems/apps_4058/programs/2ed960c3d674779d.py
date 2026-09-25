import sys

def min_heaters_to_warm_up_house(n, r, house):
    heaters = [i for i in range(n) if house[i] == 1]
    if not heaters:
        return -1
    
    heaters_needed = 0
    current_pos = 0
    
    while current_pos < n:
        max_reach = -1
        for heater in heaters:
            if abs(heater - current_pos) <= r:
                max_reach = max(max_reach, heater)
        
        if max_reach == -1:
            return -1
        
        heaters_needed += 1
        current_pos = max_reach + r
    
    return heaters_needed

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    r = int(data[1])
    house = list(map(int, data[2:]))
    
    result = min_heaters_to_warm_up_house(n, r, house)
    print(result)

if __name__ == "__main__":
    main()