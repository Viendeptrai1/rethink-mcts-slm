import sys

def construct_string(n, k, t):
    if k == 1:
        return t
    # Start with the first occurrence of t
    s = t
    # Add the necessary parts of t to achieve exactly k occurrences
    for i in range(1, k):
        # Append the part of t starting from the last character of the current s
        # to ensure maximum overlap
        s += t[n - (len(s) % n):]
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