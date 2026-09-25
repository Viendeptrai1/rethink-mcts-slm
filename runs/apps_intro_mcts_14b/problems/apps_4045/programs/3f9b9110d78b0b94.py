import sys

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    s = data[1]
    t = data[2]
    
    if s == t:
        if s == "aa" or s == "bb" or s == "cc":
            print("NO")
            return
        else:
            res = "a" * n + "b" * n + "c" * n
            print("YES")
            print(res)
            return
    
    if s[0] == t[0] and s[1] == t[1]:
        if s[0] == s[1]:
            print("NO")
            return
        else:
            res = "a" * n + "b" * n + "c" * n
            print("YES")
            print(res)
            return
    
    if s[0] == t[1] and s[1] == t[0]:
        if s[0] == s[1]:
            print("NO")
            return
        else:
            res = "a" * n + "b" * n + "c" * n
            print("YES")
            print(res)
            return
    
    res = []
    for i in range(n):
        if i % 3 == 0:
            res.append('a')
        elif i % 3 == 1:
            res.append('b')
        else:
            res.append('c')
    
    res_str = ''.join(res)
    
    if s in res_str or t in res_str:
        print("NO")
    else:
        print("YES")
        print(res_str)

if __name__ == "__main__":
    main()