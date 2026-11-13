import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    
    if not data:
        return
    
    n = int(data[0])
    a = []
    
    # Parse the N integers
    for i in range(n):
        a.append(int(data[i + 1]))
    
    # Sort in descending order to quickly find largest pairs
    a.sort(reverse=True)
    
    max_area = 0
    prev_length = -1
    
    # Iterate through the sorted array to find the largest pairs
    for i in range(n - 1):
        if a[i] == a[i + 1]:
            # Found a pair
            length = a[i]
            if length == prev_length:
                # We already used this length for a pair, so we have 4 sticks of this length
                # This forms a square with area length * length
                max_area = max(max_area, length * length)
                # No need to check further for this length as we want maximum
                break
            else:
                # New pair, check area
                max_area = max(max_area, length * length)
                prev_length = length
        else:
            prev_length = -1
            
    # If we didn't find any pair of pairs yet, we might have missed a case where
    # the two largest pairs are different lengths. Let's do a more robust approach.
    
    # Reset and do a proper two-pass or single pass with state
    # Actually, let's restart with a cleaner logic
    
    a.sort(reverse=True)
    
    pairs = []
    for i in range(n - 1):
        if a[i] == a[i + 1]:
            pairs.append(a[i])
            i += 1  # Skip the next one as it's part of the same pair
    
    # Now we have a list of lengths that can form one side of a rectangle
    # Sort pairs in descending order
    pairs.sort(reverse=True)
    
    if len(pairs) >= 2:
        # The largest rectangle is formed by the two largest pairs
        max_area = pairs[0] * pairs[1]
    else:
        max_area = 0
        
    print(max_area)

if __name__ == "__main__":
    solve()