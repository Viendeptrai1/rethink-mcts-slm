import sys

def main():
    line = sys.stdin.readline().strip()
    A, B = map(float, line.split())
    result = int(A * B)
    print(result)

if __name__ == "__main__":
    main()