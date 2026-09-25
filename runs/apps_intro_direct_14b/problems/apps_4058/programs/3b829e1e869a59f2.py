import sys

def min_heaters_to_warm_up_house(n, r, house):
    heaters = [i for i in range(n) if house[i] == 1]
    if not heaters:
        return -1
    
    heaters_needed = 0
    current_coverage = -1
    
    for heater in heaters:
        if heater > current_coverage:
            heaters_needed += 1
            current_coverage = heater + r - 1
    
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