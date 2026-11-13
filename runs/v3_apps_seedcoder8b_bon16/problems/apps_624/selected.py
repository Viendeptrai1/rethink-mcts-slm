import sys
import heapq

def max_average_power(n, k, m, powers):
    # Create a min-heap with tuples of (power, index)
    min_heap = [(power, i) for i, power in enumerate(powers)]
    heapq.heapify(min_heap)
    
    # Use operations to increase powers of least powerful superheroes
    for _ in range(m):
        if not min_heap:
            break
        power, idx = heapq.heappop(min_heap)
        power += 1
        heapq.heappush(min_heap, (power, idx))
    
    # Calculate the sum of all remaining powers
    total_power = sum(power for power, _ in min_heap)
    return total_power / n

def main():
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    k = int(data[1])
    m = int(data[2])
    powers = list(map(int, data[3:3+n]))
    
    result = max_average_power(n, k, m, powers)
    print(result)

if __name__ == "__main__":
    main()