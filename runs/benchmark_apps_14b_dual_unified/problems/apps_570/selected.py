import sys

def main():
    import sys
    a, b = map(int, sys.stdin.readline().split())
    turn = 1
    while True:
        if turn % 2 == 1:  # Vladik's turn
            if a < turn:
                print("Vladik")
                return
            a -= turn
        else:  # Valera's turn
            if b < turn:
                print("Valera")
                return
            b -= turn
        turn += 1

if __name__ == "__main__":
    main()