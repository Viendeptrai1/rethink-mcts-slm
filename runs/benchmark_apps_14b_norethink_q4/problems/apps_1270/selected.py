import sys

def main():
    import sys
    n = int(sys.stdin.read())
    
    if n == 2:
        print(1)
        print(2)
    elif n == 3:
        print(1)
        print(3)
    else:
        if n % 2 == 0:
            k = n // 2
            print(k)
            print(" ".join(["2"] * k))
        else:
            k = (n - 3) // 2 + 1
            print(k)
            print("2 " * (k - 1) + "3")

if __name__ == "__main__":
    main()