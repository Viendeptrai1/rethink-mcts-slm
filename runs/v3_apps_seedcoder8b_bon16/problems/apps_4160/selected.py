def years_to_reach_balance(X):
    balance = 100
    years = 0
    while balance < X:
        balance = int(balance * 1.01)
        years += 1
    return years

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    X = int(input().strip())
    print(years_to_reach_balance(X))