def count_grey_cells(R, C, K):
    def is_white(row, col):
        return '1' not in bin(row)[2:] and '1' not in bin(col)[2:]
    
    grey_count = 0
    row, col = 0, 0
    direction = 1
    
    while True:
        if is_white(row, col):
            grey_count += 1
        
        if grey_count == K:
            break
        
        col += direction
        if col >= C or col < 0:
            col -= direction
            row += 1
            direction *= -1
    
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