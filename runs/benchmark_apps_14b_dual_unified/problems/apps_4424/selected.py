import sys

def main():
    input = sys.stdin.read().split()
    K = int(input[0])
    X = int(input[1])
    
    if K * 500 >= X:
        print("Yes")
    else:
        print("No")

if __name__ == "__main__":
    main()