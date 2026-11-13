def check_word_chain(A, B, C):
    if A[-1] == B[0] and B[-1] == C[0]:
        return "YES"
    else:
        return "NO"

# Read input from standard input
A, B, C = input().split()

# Call the function and print the result
print(check_word_chain(A, B, C))