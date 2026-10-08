import sys

def main():
    # Read input from standard input
    T, X = map(int, sys.stdin.read().split())
    
    # Calculate the number of hours that will pass in World A
    hours_in_world_A = T / X
    
    # Print the result with the required precision
    print(f"{hours_in_world_A:.10f}")

if __name__ == "__main__":
    main()