def main():
    import sys
    input = sys.stdin.read
    S = input().strip()
    
    # Base price of the bowl of ramen
    base_price = 700
    
    # Calculate the number of toppings
    num_toppings = S.count('o')
    
    # Calculate the total price
    total_price = base_price + 100 * num_toppings
    
    # Print the total price
    print(total_price)

if __name__ == "__main__":
    main()