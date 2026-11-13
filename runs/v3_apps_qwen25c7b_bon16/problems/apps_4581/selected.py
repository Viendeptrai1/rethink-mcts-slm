import sys

def calculate_ramen_price(s):
    base_price = 700
    topping_price_per_kind = 100
    num_toppings = s.count('o')
    total_price = base_price + (num_toppings * topping_price_per_kind)
    return total_price

if __name__ == "__main__":
    s = sys.stdin.read().strip()
    print(calculate_ramen_price(s))