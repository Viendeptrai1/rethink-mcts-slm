import sys

def main():
    input = sys.stdin.read().split()
    A = int(input[0])
    B = float(input[1])
    result = int(A * B)
    print(result)

if __name__ == "__main__":
    main()