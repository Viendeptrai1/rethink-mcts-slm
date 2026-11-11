import sys

def calculate_min_time(n, m, candies):
    def distance(start, end):
        return min(abs(start - end), n - abs(start - end))
    
    result = []
    
    for start_station in range(1, n + 1):
        total_time = 0
        current_station = start_station
        
        for candy in sorted(candies, key=lambda x: distance(current_station, x[0])):
            a_i, b_i = candy
            # Move to the station where the candy is
            total_time += distance(current_station, a_i)
            current_station = a_i
            # Load the candy
            # Move to the destination station
            total_time += distance(a_i, b_i)
            current_station = b_i
            # Deliver the candy
        
        result.append(total_time)
    
    return result

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    index = 0
    n = int(data[index])
    index += 1
    m = int(data[index])
    index += 1
    
    candies = []
    for _ in range(m):
        a_i = int(data[index])
        index += 1
        b_i = int(data[index])
        index += 1
        candies.append((a_i, b_i))
    
    result = calculate_min_time(n, m, candies)
    print(" ".join(map(str, result)))

if __name__ == "__main__":
    main()