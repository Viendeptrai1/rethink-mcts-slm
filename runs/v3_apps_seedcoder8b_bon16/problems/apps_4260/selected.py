def main():
    import sys
    input = sys.stdin.read
    data = input().strip()
    T, X = map(int, data.split())
    hours_in_world_a = T / X
    print(f"{hours_in_world_a:.10f}")

if __name__ == "__main__":
    main()