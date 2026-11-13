import sys

def can_buy(K, X):
    total_value = K * 500
    return "Yes" if total_value >= X else "No"

if __name__ == "__main__":
    input = sys.stdin.read
    data = input().split()
    K = int(data[0])
    X = int(data[1])
    result = can_buy(K, X)
    print(result)