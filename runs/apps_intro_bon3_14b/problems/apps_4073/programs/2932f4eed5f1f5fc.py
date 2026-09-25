import sys

def main():
    import sys

    # Read input
    n = int(sys.stdin.readline().strip())
    a = list(map(int, sys.stdin.readline().strip().split()))

    # Calculate the result
    result = 0
    for ai in a:
        result ^= ai

    # Print the result
    print(result)

if __name__ == "__main__":
    main()