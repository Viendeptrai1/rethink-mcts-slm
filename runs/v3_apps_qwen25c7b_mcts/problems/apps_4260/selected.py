import sys

def calculate_time_in_world_a(T, X):
    return T / X

if __name__ == "__main__":
    input = sys.stdin.read
    data = input().split()
    T = int(data[0])
    X = int(data[1])
    result = calculate_time_in_world_a(T, X)
    print(f"{result:.10f}")