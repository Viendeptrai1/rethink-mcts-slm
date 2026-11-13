import sys

def minimize_unusefulness():
    N = int(input())
    x_coords = []
    y_coords = []
    
    for _ in range(N):
        x, y = map(int, input().split())
        x_coords.append(x)
        y_coords.append(y)
    
    x_coords.sort()
    y_coords.sort()
    
    if N % 2 == 1:
        median_x = x_coords[N // 2]
        median_y = y_coords[N // 2]
    else:
        median_x = (x_coords[N // 2 - 1] + x_coords[N // 2]) / 2
        median_y = (y_coords[N // 2 - 1] + y_coords[N // 2]) / 2
    
    a = median_y - median_x
    
    print(f"{a:.6f}")

if __name__ == "__main__":
    minimize_unusefulness()