import sys

def main():
    a = int(input().strip())
    if 10 <= a <= 999:
        print(1)
    else:
        print(0)

if __name__ == "__main__":
    main()