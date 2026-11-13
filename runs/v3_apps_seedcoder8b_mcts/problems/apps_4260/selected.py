def calculate_hours_in_world_a(T, X):
    # Calculate the time passed in World A
    hours_in_world_a = T / X
    # Print the result with high precision
    print(f"{hours_in_world_a:.10f}")

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().strip()
    T, X = map(int, data.split())
    calculate_hours_in_world_a(T, X)