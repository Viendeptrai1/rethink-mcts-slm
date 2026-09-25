import sys

def find_price(A, B):
    for price in range(1, 10001):  # Arbitrary large upper limit
        tax_8_percent = (price * 8) // 100
        tax_10_percent = (price * 10) // 100
        if tax_8_percent == A and tax_10_percent == B:
            return price
    return -1

def main():
    import sys
    input = sys.stdin.read().strip().split()
    A = int(input[0])
    B = int(input[1])
    result = find_price(A, B)
    print(result)

if __name__ == "__main__":
    main()