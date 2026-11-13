def main():
    import sys
    input = sys.stdin.read
    data = input().strip()
    A, B = data.split()
    A = int(A)
    B = float(B)
    result = int(A * B)
    print(result)

if __name__ == "__main__":
    main()