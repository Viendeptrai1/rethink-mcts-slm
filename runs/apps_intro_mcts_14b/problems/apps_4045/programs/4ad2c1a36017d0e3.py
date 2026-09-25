import sys

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    s = data[1]
    t = data[2]
    
    if s == "ab" and t == "bc":
        print("NO")
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