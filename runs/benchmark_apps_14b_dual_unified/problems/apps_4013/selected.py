import sys
import heapq

def main():
    import sys
    import heapq
    
    def readints():
        return list(map(int, sys.stdin.readline().split()))
    
    n = int(sys.stdin.readline())
    a = readints()
    
    if n == 2:
        print(0)
        return
    
    # Find the minimum and maximum values in the array
    min_val = min(a)
    max_val = max(a)
    
    # Count occurrences of min and max values
    min_count = a.count(min_val)
    max_count = a.count(max_val)
    
    # If there are multiple min or max values, we can remove one of them
    if min_count > 1 or max_count > 1:
        print(max_val - min_val)
        return
    
    # Otherwise, we need to consider removing either the min or max value
    # Calculate the instability if we remove the min value
    a.remove(min_val)
    max_after_remove_min = max(a)
    instability_remove_min = max_after_remove_min - min(a)
    
    # Calculate the instability if we remove the max value
    a.append(min_val)  # Add back the min value
    a.remove(max_val)
    min_after_remove_max = min(a)
    instability_remove_max = max(a) - min_after_remove_max
    
    # Print the minimum of the two possible instabilities
    print(min(instability_remove_min, instability_remove_max))

if __name__ == "__main__":
    main()