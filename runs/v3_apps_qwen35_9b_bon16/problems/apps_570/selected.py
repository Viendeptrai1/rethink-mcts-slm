import sys

def solve():
    try:
        line = sys.stdin.readline()
        if not line:
            return
        parts = line.strip().split()
        if len(parts) != 2:
            return
        a = int(parts[0])
        b = int(parts[1])
    except ValueError:
        return

    turn = 1
    while True:
        if turn % 2 == 1:
            # Vladik's turn, needs to give 'turn' candies
            if a < turn:
                print("Vladik")
                return
            a -= turn
            turn += 1
        else:
            # Valera's turn, needs to give 'turn' candies
            if b < turn:
                print("Valera")
                return
            b -= turn
            turn += 1

if __name__ == "__main__":
    solve()