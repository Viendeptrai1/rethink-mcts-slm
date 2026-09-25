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
    if (x3 < x2 and x4 > x1 and y3 < y2 and y4 > y1) or (x5 < x2 and x6 > x1 and y5 < y2 and y6 > y1):
        return True
    
    return False

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    x1, y1, x2, y2 = map(int, data[0:4])
    x3, y3, x4, y4 = map(int, data[4:8])
    x5, y5, x6, y6 = map(int, data[8:12])
    
    if is_visible(x1, y1, x2, y2, x3, y3, x4, y4, x5, y5, x6, y6):
        print("YES")
    else:
        print("NO")

if __name__ == "__main__":
    main()