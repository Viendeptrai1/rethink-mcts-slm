import sys

def main():
    # Read input from standard input
    A = list(map(int, sys.stdin.readline().split()))
    
    # Sort the tasks by their values
    A.sort()
    
    # Calculate the minimum total cost
    cost = abs(A[1] - A[0]) + abs(A[2] - A[1])
    
    # Print the result
    print(cost)

if __name__ == "__main__":
    main()