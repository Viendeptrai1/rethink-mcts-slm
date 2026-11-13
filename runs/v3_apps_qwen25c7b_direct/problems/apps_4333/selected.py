import sys

def main():
    input = sys.stdin.read
    data = input().split()
    
    x1, y1, x2, y2 = map(int, data)
    
    # Calculate the side length of the square
    side_length = abs(x2 - x1)
    
    # Determine the direction of the square based on the first two points
    if y2 > y1:
        # Square is oriented upwards
        x3, y3 = x1 + side_length, y1
        x4, y4 = x1, y1 + side_length
    else:
        # Square is oriented downwards
        x3, y3 = x1, y1 - side_length
        x4, y4 = x1 - side_length, y1
    
    print(f"{x3} {y3} {x4} {y4}")

if __name__ == "__main__":
    main()