import sys

def main():
    X = int(sys.stdin.read().strip())
    balance = 100
    years = 0
    
    while balance < X:
        balance = balance * 1.01
        balance = int(balance)  # Discard the fraction of less than one yen
        years += 1
    
    print(years)

if __name__ == "__main__":
    main()