import sys

def main():
    input = sys.stdin.read
    data = input().split()
    K = int(data[0])
    X = int(data[1])
    
    if K * 500 >= X:
        print("Yes")
    else:
        print("No")

if __name__ == "__main__":
    main()