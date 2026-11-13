def check_takahashi_statement():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    c = [[int(data[3*i + j]) for j in range(3)] for i in range(3)]
    
    # Check if we can find a_1, a_2, a_3, b_1, b_2, b_3
    for a1 in range(101):
        for a2 in range(101):
            for a3 in range(101):
                for b1 in range(101):
                    for b2 in range(101):
                        for b3 in range(101):
                            if (a1 + b1 == c[0][0] and
                                a1 + b2 == c[0][1] and
                                a1 + b3 == c[0][2] and
                                a2 + b1 == c[1][0] and
                                a2 + b2 == c[1][1] and
                                a2 + b3 == c[1][2] and
                                a3 + b1 == c[2][0] and
                                a3 + b2 == c[2][1] and
                                a3 + b3 == c[2][2]):
                                print("Yes")
                                return
    print("No")

check_takahashi_statement()