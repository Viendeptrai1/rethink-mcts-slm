import sys

def solve():
    input = sys.stdin.read
    data = input().split()
    
    x1, y1, x2, y2 = map(int, data[0:4])
    x3, y3, x4, y4 = map(int, data[4:8])
    x5, y5, x6, y6 = map(int, data[8:12])
    
    white_area = (x2 - x1) * (y2 - y1)
    if white_area == 0:
        print("NO")
        return

    # Calculate overlap between white and black1
    i1 = max(x1, x3)
    j1 = max(y1, y3)
    i2 = min(x2, x4)
    j2 = min(y2, y4)
    
    area1 = 0
    if i2 > i1 and j2 > j1:
        area1 = (i2 - i1) * (j2 - j1)

    # Calculate overlap between white and black2
    i3 = max(x1, x5)
    j3 = max(y1, y5)
    i4 = min(x2, x6)
    j4 = min(y2, y6)
    
    area2 = 0
    if i4 > i3 and j4 > j3:
        area2 = (i4 - i3) * (j4 - j3)

    # Calculate overlap between black1 and black2
    i5 = max(x3, x5)
    j5 = max(y3, y5)
    i6 = min(x4, x6)
    j6 = min(y4, y6)
    
    area3 = 0
    if i6 > i5 and j6 > j5:
        area3 = (i6 - i5) * (j6 - j5)

    # Calculate overlap between (white & black1) and (white & black2)
    # This is equivalent to overlap between white and (black1 & black2)
    i7 = max(i1, i3)
    j7 = max(j1, j3)
    i8 = min(i2, i4)
    j8 = min(j2, j4)
    
    area_overlap = 0
    if i8 > i7 and j8 > j7:
        area_overlap = (i8 - i7) * (j8 - j7)

    # Total covered area = area1 + area2 - area_overlap
    covered = area1 + area2 - area_overlap

    if covered < white_area:
        print("YES")
    else:
        print("NO")

if __name__ == "__main__":
    solve()