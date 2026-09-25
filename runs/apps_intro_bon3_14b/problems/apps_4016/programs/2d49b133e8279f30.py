import sys

def construct_string(n, k, t):
    if k == 1:
        return t
    else:
        # We need to place t k times in s
        # The minimum length of s is when we overlap t as much as possible
        # We can achieve this by placing t and then adding one character from t at the end
        # This way, the last character of the previous t overlaps with the first character of the next t
        return t * (k - 1) + t[0]

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