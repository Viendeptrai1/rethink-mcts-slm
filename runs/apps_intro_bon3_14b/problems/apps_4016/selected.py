import sys

def construct_string(n, k, t):
    if k == 1:
        return t
    # We need to find the minimum length of s such that t appears exactly k times as a substring.
    # The optimal way to do this is to overlap t as much as possible.
    # If k is greater than 1, we can start with t and then append t[1:] repeatedly.
    # This way, each new t[1:] will overlap with the previous t by n-1 characters.
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
    sys.stdout.write(result)

if __name__ == "__main__":
    main()