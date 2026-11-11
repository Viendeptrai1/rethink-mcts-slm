import sys

def main():
    import sys

    def read_ints():
        return list(map(int, sys.stdin.readline().split()))

    x1, y1, x2, y2 = read_ints()
    x3, y3, x4, y4 = read_ints()
    x5, y5, x6, y6 = read_ints()

    # Check if the white sheet is completely covered by the first black sheet
    if x3 <= x1 and y3 <= y1 and x4 >= x2 and y4 >= y2:
        print("NO")
        return

    # Check if the white sheet is completely covered by the second black sheet
    if x5 <= x1 and y5 <= y1 and x6 >= x2 and y6 >= y2:
        print("NO")
        return

    # Check if the white sheet is completely covered by both black sheets
    if (x3 <= x1 and y3 <= y1 and x4 >= x2 and y4 >= y2) or (x5 <= x1 and y5 <= y1 and x6 >= x2 and y6 >= y2):
        print("NO")
        return

    # Check if there is any part of the white sheet that is not covered by either black sheet
    if (x3 < x2 and x4 > x1 and y3 < y2 and y4 > y1) or (x5 < x2 and x6 > x1 and y5 < y2 and y6 > y1):
        print("YES")
    else:
        print("NO")

if __name__ == "__main__":
    main()