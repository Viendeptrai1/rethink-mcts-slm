def min_rows_for_mirror(a):
    n = len(a)
    m = len(a[0])
    
    # Create a set to store unique rows
    unique_rows = set()
    
    # Add each row of the matrix to the set
    for row in a:
        unique_rows.add(tuple(row))
    
    # Calculate the minimum number of rows needed
    min_rows = len(unique_rows)
    
    return min_rows

# Example usage
if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    m = int(data[1])
    
    a = []
    index = 2
    for _ in range(n):
        row = list(map(int, data[index:index+m]))
        a.append(row)
        index += m
    
    result = min_rows_for_mirror(a)
    print(result)