import sys

def is_visible(x1, y1, x2, y2, x3, y3, x4, y4, x5, y5, x6, y6):
    # Check if the white sheet is completely covered by the first black sheet
    if x3 <= x1 and y3 <= y1 and x4 >= x2 and y4 >= y2:
        return False
    
    # Check if the white sheet is completely covered by the second black sheet
    if x5 <= x1 and y5 <= y1 and x6 >= x2 and y6 >= y2:
        return False
    
    # Check if the white sheet is completely covered by both black sheets
    if (x3 <= x1 and y3 <= y1 and x4 >= x2 and y4 >= y2) or (x5 <= x1 and y5 <= y1 and x6 >= x2 and y6 >= y2):
        return False
    
    # Check if there is any part of the white sheet not covered by the black sheets
    # Calculate the intersection of the white sheet with the first black sheet
    x_left = max(x1, x3)
    y_left = max(y1, y3)
    x_right = min(x2, x4)
    y_right = min(y2, y4)
    
    # Calculate the intersection of the white sheet with the second black sheet
    x_left2 = max(x1, x5)
    y_left2 = max(y1, y5)
    x_right2 = min(x2, x6)
    y_right2 = min(y2, y6)
    
    # Check if the intersection with the first black sheet is valid
    if x_left < x_right and y_left < y_right:
        # Check if the intersection with the second black sheet is valid
        if x_left2 < x_right2 and y_left2 < y_right2:
            # Check if the intersection of both black sheets covers the white sheet
            x_overlap = max(x_left, x_left2)
            y_overlap = max(y_left, y_left2)
            x_overlap2 = min(x_right, x_right2)
            y_overlap2 = min(y_right, y_right2)
            
            if x_overlap < x_overlap2 and y_overlap < y_overlap2:
                return False
    
    return True

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    x1, y1, x2, y2 = map(int, data[:4])
    x3, y3, x4, y4 = map(int, data[4:8])
    x5, y5, x6, y6 = map(int, data[8:])
    
    if is_visible(x1, y1, x2, y2, x3, y3, x4, y4, x5, y5, x6, y6):
        print("YES")
    else:
        print("NO")

if __name__ == "__main__":
    main()