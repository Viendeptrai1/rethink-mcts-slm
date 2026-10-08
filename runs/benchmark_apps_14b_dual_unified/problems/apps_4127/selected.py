import sys

def main():
    input = sys.stdin.read
    data = input().split()
    A = int(data[0])
    B = float(data[1])
    result = int(A * B)
    print(result)

if __name__ == "__main__":
    main()