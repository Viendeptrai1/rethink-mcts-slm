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
    
    res = []
    for i in range(n):
        res.append('a')
        res.append('b')
        res.append('c')
    
    res_str = ''.join(res)
    
    if s in res_str or t in res_str:
        print("NO")
    else:
        print("YES")
        print(res_str)

if __name__ == "__main__":
    main()