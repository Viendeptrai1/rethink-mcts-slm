s = input()
base_price = 700
topping_count = s.count('o')
total_price = base_price + topping_count * 100
print(total_price)