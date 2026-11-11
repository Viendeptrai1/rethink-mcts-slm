import sys

def main():
    input = sys.stdin.read
    data = input().split()
    
    # Convert input strings to integers
    c = [[int(data[i*3 + j]) for j in range(3)] for i in range(3)]
    
    # Check row differences
    for i in range(3):
        diff = c[i][1] - c[i][0]
        if c[i][2] - c[i][1] != diff:
            print("No")
            return
    
    # Check column differences
    for j in range(3):
        diff = c[1][j] - c[0][j]
        if c[2][j] - c[1][j] != diff:
            print("No")
            return
    
    print("Yes")

if __name__ == "__main__":
    main()