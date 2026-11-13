def main():
    import sys
    input = sys.stdin.read
    X = int(input().strip())
    
    balance = 100
    years = 0
    
    while balance < X:
        balance += balance * 0.01
        years += 1
    
    print(years)

if __name__ == "__main__":
    main()