import sys

def construct_string(n, k, t):
    if k == 1:
        return t
    else:
        # We need to place t k times in s
        # The minimum length of s will be (k-1)*(n-1) + n
        # This is because we can overlap t by (n-1) characters each time
        s = t
        for _ in range(1, k):
            s += t[1:]
        return s

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    k = int(data[1])
    t = data[2]
    
    result = construct_string(n, k, t)
    print(result)

if __name__ == "__main__":
    main()