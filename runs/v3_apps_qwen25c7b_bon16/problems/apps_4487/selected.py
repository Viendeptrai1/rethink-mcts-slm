def check_word_chain(A, B, C):
    if A[-1] == B[0] and B[-1] == C[0]:
        return "YES"
    else:
        return "NO"

# Input reading
A, B, C = input().split()

# Function call and result printing
print(check_word_chain(A, B, C))