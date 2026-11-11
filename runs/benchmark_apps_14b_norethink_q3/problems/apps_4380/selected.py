import sys

def main():
    input = sys.stdin.read
    data = input().split()
    A = int(data[0])
    B = int(data[1])
    
    if A % 2 == 1 and B % 2 == 1:
        print("Yes")
    else:
        print("No")

if __name__ == "__main__":
    main()