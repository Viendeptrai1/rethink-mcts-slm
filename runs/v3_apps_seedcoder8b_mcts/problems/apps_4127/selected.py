def main():
    import sys
    input = sys.stdin.read
    data = input().strip()
    A, B = data.split()
    A = int(A)
    B = int(float(B) * 100)
    result = (A * B) // 100
    print(result)

if __name__ == "__main__":
    main()