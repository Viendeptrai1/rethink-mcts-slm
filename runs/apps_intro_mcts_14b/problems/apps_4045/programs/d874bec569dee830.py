import sys

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    s = data[1]
    t = data[2]
    
    if s == "ab" and t == "bc":
        if n == 1:
            print("NO")
        else:
            print("YES")
            print("ac" + "ba" * (n - 1))
    elif s == "bc" and t == "ab":
        if n == 1:
            print("NO")
        else:
            print("YES")
            print("ba" + "ac" * (n - 1))
    else:
        print("YES")
        print("abc" * n)

if __name__ == "__main__":
    main()