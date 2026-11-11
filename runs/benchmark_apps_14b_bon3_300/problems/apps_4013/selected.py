import sys
import heapq

def main():
    import sys
    import heapq
    
    def read_ints():
        return list(map(int, sys.stdin.read().split()))
    
    data = read_ints()
    n = data[0]
    a = data[1:]
    
    # Sort the array
    a.sort()
    
    # Calculate the initial instability
    initial_instability = a[-1] - a[0]
    
    # If all elements are the same, the instability is already 0
    if initial_instability == 0:
        print(0)
        return
    
    # Calculate the minimum instability by removing one element
    min_instability = float('inf')
    
    # Remove the smallest element
    min_instability = min(min_instability, a[-1] - a[1])
    
    # Remove the largest element
    min_instability = min(min_instability, a[n-2] - a[0])
    
    # Remove any other element
    for i in range(1, n-1):
        min_instability = min(min_instability, a[i-1] - a[0])
        min_instability = min(min_instability, a[n-1] - a[i+1])
    
    print(min_instability)

if __name__ == "__main__":
    main()