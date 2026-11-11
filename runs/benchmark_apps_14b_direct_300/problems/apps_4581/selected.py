import sys

def calculate_ramen_price(S):
    base_price = 700
    topping_price = 100
    price = base_price
    
    for char in S:
        if char == 'o':
            price += topping_price
    
    return price

if __name__ == "__main__":
    S = sys.stdin.read().strip()
    print(calculate_ramen_price(S))