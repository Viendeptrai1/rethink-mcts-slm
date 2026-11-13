def calculate_ramen_price(S):
    base_price = 700
    topping_count = S.count('o')
    return base_price + 100 * topping_count

# Example usage
import sys
input = sys.stdin.read().strip()
print(calculate_ramen_price(input))