import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    a = int(input_data[0])
    b = int(input_data[1])

    k = 1
    while True:
        if a < k:
            print("Valera")
            return
        a -= k
        k += 1
        if b < k:
            print("Vladik")
            return
        b -= k
        k += 1

if __name__ == "__main__":
    solve()