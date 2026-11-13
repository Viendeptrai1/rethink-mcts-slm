def calculate_ramen_price(S):
    base_price = 700
    topping_price = 100
    num_toppings = 0
    
    if S[0] == 'o':
        num_toppings += 1
    if S[1] == 'o':
        num_toppings += 1
    if S[2] == 'o':
        num_toppings += 1
        
    total_price = base_price + (topping_price * num_toppings)
    print(total_price)

# Reading input
import sys
input = sys.stdin.read().strip()
calculate_ramen_price(input)