def count_grey_cells(R, C, K):
    def has_common_one_bit(x, y):
        return (x & y) != 0
    
    grey_count = 0
    for i in range(K):
        row = i // C
        col = i % C
        if has_common_one_bit(row, col):
            grey_count += 1
    
    return grey_count

# Example usage:
import sys
input = sys.stdin.read
data = input().split()
R = int(data[0])
C = int(data[1])
K = int(data[2])

result = count_grey_cells(R, C, K)
print(result)