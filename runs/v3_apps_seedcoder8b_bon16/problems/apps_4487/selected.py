def check_word_chain():
    import sys
    input = sys.stdin.read
    data = input().strip()
    A, B, C = data.split()
    
    if A[-1] == B[0] and B[-1] == C[0]:
        print("YES")
    else:
        print("NO")

check_word_chain()