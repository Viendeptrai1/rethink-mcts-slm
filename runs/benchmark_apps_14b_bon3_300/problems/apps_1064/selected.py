import sys

def min_cost_to_illuminate(n, m, k, blocked_positions, lamp_costs):
    def can_illuminate_with_power(power):
        last_position = -1
        count = 0
        for i in range(n):
            if i in blocked_positions:
                continue
            if i > last_position:
                count += 1
                last_position = i + power - 1
        return last_position >= n - 1

    min_cost = float('inf')
    for power in range(1, k + 1):
        if can_illuminate_with_power(power):
            min_cost = min(min_cost, lamp_costs[power - 1])

    return min_cost if min_cost != float('inf') else -1

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    m = int(data[1])
    k = int(data[2])
    
    blocked_positions = set(map(int, data[3:3 + m]))
    
    lamp_costs = list(map(int, data[3 + m:3 + m + k]))
    
    result = min_cost_to_illuminate(n, m, k, blocked_positions, lamp_costs)
    print(result)

if __name__ == "__main__":
    main()