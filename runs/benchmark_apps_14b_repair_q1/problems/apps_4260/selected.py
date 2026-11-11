import sys

def main():
    # Read input from standard input
    input = sys.stdin.read().split()
    T = int(input[0])
    X = int(input[1])
    
    # Calculate the number of hours that will pass in World A
    hours_in_world_A = T / X
    
    # Print the result with high precision
    print(f"{hours_in_world_A:.10f}")

if __name__ == "__main__":
    main()