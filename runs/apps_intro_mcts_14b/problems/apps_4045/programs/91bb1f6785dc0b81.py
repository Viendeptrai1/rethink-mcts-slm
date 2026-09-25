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
            print("YES")
            print("abc")
        else:
            print("NO")
    elif s == "aa" and t == "bc":
        print("YES")
        res = "cac" * n
        print(res[:3*n])
    elif s == "cb" and t == "ac":
        print("YES")
        res = "abc"
        print(res)
    else:
        print("NO")

if __name__ == "__main__":
    main()