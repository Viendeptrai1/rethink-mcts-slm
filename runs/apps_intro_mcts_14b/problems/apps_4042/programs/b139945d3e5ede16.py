import sys

def main():
    import sys
    x = float(sys.stdin.read().strip())
    
    # Convert the floating-point number to an integer by multiplying by 100
    num = int(x * 100)
    
    # Ensure the number is within the valid range
    if num > 499:
        num = 499
    
    # Decompose the number into two factors
    factor1 = 1
    while factor1 <= 10:
        if num % factor1 == 0:
            factor2 = num // factor1
            if 1 <= factor2 <= 10:
                print(factor1, factor2)
                return
        factor1 += 1

if __name__ == "__main__":
    main()