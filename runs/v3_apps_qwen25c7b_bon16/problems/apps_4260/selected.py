import sys

def calculate_hours(T, X):
    return T / X

if __name__ == "__main__":
    T = int(sys.stdin.readline().strip())
    X = int(sys.stdin.readline().strip())
    result = calculate_hours(T, X)
    print(f"{result:.10f}")