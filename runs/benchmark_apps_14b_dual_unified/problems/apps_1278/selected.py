import sys

def find_earliest_not_so_rainy_day(n, x, y, rain_amounts):
    for d in range(n):
        is_not_so_rainy = True
        for j in range(max(0, d - x), d):
            if rain_amounts[d] >= rain_amounts[j]:
                is_not_so_rainy = False
                break
        for j in range(d + 1, min(n, d + y + 1)):
            if rain_amounts[d] >= rain_amounts[j]:
                is_not_so_rainy = False
                break
        if is_not_so_rainy:
            return d + 1  # Return 1-based index

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    x = int(data[1])
    y = int(data[2])
    rain_amounts = list(map(int, data[3:]))
    
    result = find_earliest_not_so_rainy_day(n, x, y, rain_amounts)
    print(result)

if __name__ == "__main__":
    main()