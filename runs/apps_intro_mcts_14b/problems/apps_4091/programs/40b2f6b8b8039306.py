import sys

def max_profit_distribution(n, k, difficulties):
    # Initialize the profit array
    profit = [0] * k
    # Initialize the distribution array
    distribution = [0] * k
    
    # Start from the end of the difficulties list
    current_index = n - 1
    
    # Assign problems to days starting from the last day
    for day in range(k - 1, -1, -1):
        # Find the maximum difficulty for the current day
        max_difficulty = 0
        max_difficulty_index = current_index
        while current_index >= 0 and current_index >= day:
            if difficulties[current_index] > max_difficulty:
                max_difficulty = difficulties[current_index]
                max_difficulty_index = current_index
            current_index -= 1
        
        # Assign the problems from max_difficulty_index to the end of the list to the current day
        distribution[day] = max_difficulty_index - day + 1
        profit[day] = max_difficulty
    
    # Calculate the total profit
    total_profit = sum(profit)
    
    return total_profit, distribution

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    k = int(data[1])
    difficulties = list(map(int, data[2:]))
    
    total_profit, distribution = max_profit_distribution(n, k, difficulties)
    
    print(total_profit)
    print(' '.join(map(str, distribution)))

if __name__ == "__main__":
    main()