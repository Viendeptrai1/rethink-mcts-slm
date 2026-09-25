import sys

def main():
    x = float(sys.stdin.read().strip())
    if x < 1.5:
        a, b = 1, 1
    elif x < 2.5:
        a, b = 2, 2
    elif x < 3.5:
        a, b = 3, 3
    elif x < 4.5:
        a, b = 4, 4
    else:
        a, b = 5, 5
    print(a, b)

if __name__ == "__main__":
    main()