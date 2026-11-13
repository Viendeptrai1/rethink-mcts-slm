import sys

def check_takahashi_statement():
    c = [list(map(int, input().split())) for _ in range(3)]
    
    # Extract first row and first column to find a_1, a_2, a_3 and b_1, b_2, b_3
    a = [c[0][0], c[0][1], c[0][2]]
    b = [c[i][0] for i in range(3)]
    
    # Check if the differences match for all elements in the grid
    for i in range(3):
        for j in range(3):
            if c[i][j] != a[j] + b[i]:
                return "No"
    return "Yes"

# Call the function and print the result
print(check_takahashi_statement())