import sys

def main():
    # Read input
    c = [list(map(int, input().split())) for _ in range(3)]
    
    # Check if the grid can be represented as a_i + b_j
    a = [c[0][0], c[1][0] - c[0][0], c[2][0] - c[0][0]]
    b = [c[0][0], c[0][1] - c[0][0], c[0][2] - c[0][0]]
    
    for i in range(3):
        for j in range(3):
            if c[i][j] != a[i] + b[j]:
                print("No")
                return
    
    print("Yes")

if __name__ == "__main__":
    main()