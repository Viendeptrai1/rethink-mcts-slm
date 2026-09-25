import sys

def min_heaters_to_warm_up_house(n, r, house):
    heaters = [i for i in range(n) if house[i] == 1]
    if not heaters:
        return -1
    
    count = 0
    i = 0
    while i < n:
        found = False
        for j in range(len(heaters)):
            if heaters[j] - r <= i <= heaters[j] + r:
                found = True
                i = heaters[j] + r + 1
                count += 1
                break
        if not found:
            return -1
    return count

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