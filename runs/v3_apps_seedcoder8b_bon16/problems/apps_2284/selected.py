def minimum_cost_of_preparation_and_printing(n, k, preparation_costs, printing_costs):
    # Create a list of tuples where each tuple is (cost to prepare and print, day index)
    combined_costs = [(preparation_costs[i] + printing_costs[i], i) for i in range(n)]
    
    # Sort the combined costs based on cost in ascending order
    combined_costs.sort()
    
    # Select the first k elements from the sorted list
    # These are the k days with the minimum combined preparation and printing costs
    selected_days = sorted(combined_costs[:k], key=lambda x: x[1])
    
    # Calculate the total minimum cost
    total_cost = sum(cost for cost, _ in selected_days)
    
    return total_cost

# Example usage
if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    k = int(data[1])
    preparation_costs = list(map(int, data[2:n+2]))
    printing_costs = list(map(int, data[n+2:2*n+2]))
    
    print(minimum_cost_of_preparation_and_printing(n, k, preparation_costs, printing_costs))