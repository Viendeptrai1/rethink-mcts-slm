import sys

def main():
    import sys
    import bisect
    
    # Read input
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    difficulties = list(map(int, data[1:]))
    
    # Sort the difficulties
    difficulties.sort()
    
    # The number of problems for ARCs and ABCs should be N // 2
    target_count = N // 2
    
    # Initialize the count of valid K
    valid_K_count = 0
    
    # Iterate over possible values of K
    for i in range(N):
        # Calculate the number of problems with difficulty >= difficulties[i]
        arc_count = N - i
        
        # Calculate the number of problems with difficulty < difficulties[i]
        abc_count = i
        
        # Check if the counts are equal
        if arc_count == abc_count:
            valid_K_count += 1
    
    # Print the result
    print(valid_K_count)

if __name__ == "__main__":
    main()