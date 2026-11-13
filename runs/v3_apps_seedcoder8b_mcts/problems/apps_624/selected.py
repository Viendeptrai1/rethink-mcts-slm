import sys
import heapq

def maximize_average_power(n, k, m, powers):
    # Create a min-heap to keep track of the smallest power values
    min_heap = [(power, i) for i, power in enumerate(powers)]
    heapq.heapify(min_heap)
    
    # Operations counter
    operations_used = 0
    
    # Increase the power of the weakest superheroes first
    while operations_used < m and min_heap:
        power, index = heapq.heappop(min_heap)
        if operations_used < k:
            power += 1
            operations_used += 1
        else:
            # If we've reached the maximum operations for a single superhero,
            # we can't increase this one further, so we stop
            break
        heapq.heappush(min_heap, (power, index))
    
    # Calculate the total power after operations
    total_power = sum(power for power, _ in min_heap)
    
    # Calculate the maximum average
    max_average = total_power / n
    
    return max_average

def main():
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    k = int(data[1])
    m = int(data[2])
    powers = list(map(int, data[3:3+n]))
    
    result = maximize_average_power(n, k, m, powers)
    print(f"{result:.15f}")

if __name__ == "__main__":
    main()