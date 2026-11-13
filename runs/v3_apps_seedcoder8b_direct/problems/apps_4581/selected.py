def main():
    import sys
    input = sys.stdin.read
    S = input().strip()
    
    base_price = 700
    topping_price = 100
    topping_count = 0
    
    if S[0] == 'o':
        topping_count += 1
    if S[1] == 'o':
        topping_count += 1
    if S[2] == 'o':
        topping_count += 1
    
    total_price = base_price + topping_count * topping_price
    print(total_price)

if __name__ == "__main__":
    main()