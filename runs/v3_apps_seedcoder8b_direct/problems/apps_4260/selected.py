def calculate_hours_in_world_a(T, X):
    hours_in_world_a = T / X
    print(hours_in_world_a)

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().strip()
    T, X = map(int, data.split())
    calculate_hours_in_world_a(T, X)