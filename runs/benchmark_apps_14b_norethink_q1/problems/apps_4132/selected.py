import sys

def main():
    import sys
    import random

    def min_final_health(N, A):
        # Check if there is any odd health value
        has_odd = any(a % 2 != 0 for a in A)
        
        # If there is an odd health value, the final health can be 1
        if has_odd:
            return 1
        
        # If all health values are even, the final health will be even
        # The minimum even number is 2
        return 2

    # Read input
    N = int(sys.stdin.readline().strip())
    A = list(map(int, sys.stdin.readline().strip().split()))
    
    # Calculate and print the minimum possible final health
    print(min_final_health(N, A))

if __name__ == "__main__":
    main()