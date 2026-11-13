import sys

def main():
    input = sys.stdin.read
    data = input().split()
    A = int(data[0])
    B = int(data[1])

    if 1 <= A <= 9 and 1 <= B <= 9:
        print(A * B)
    else:
        print(-1)

if __name__ == "__main__":
    main()