import sys

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    s = data[1]
    t = data[2]
    
    # Check if it's possible to construct such a string
    if s == "ab" and t == "ba":
        print("NO")
        return
    
    # Construct the result string
    res = []
    for i in range(n):
        res.append('a')
        res.append('b')
        res.append('c')
    
    # Convert list to string
    res_str = ''.join(res)
    
    # Check if s or t is a substring of res_str
    if s in res_str or t in res_str:
        print("NO")
    else:
        print("YES")
        print(res_str)

if __name__ == "__main__":
    main()