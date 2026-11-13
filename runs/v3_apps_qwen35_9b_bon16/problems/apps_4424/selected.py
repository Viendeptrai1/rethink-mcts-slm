import sys

def main():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    K = int(input_data[0])
    X = int(input_data[1])
    if K * 500 >= X:
        print("Yes")
    else:
        print("No")

if __name__ == "__main__":
    main()