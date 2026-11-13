def max_liked_segments(n, k, a):
    # The maximum number of segments that Vanya likes is 2n - 1.
    # This is because each element can either be the start or end of a segment.
    return 2 * n - 1

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    k = int(data[1])
    a = list(map(int, data[2:2 + n]))
    
    result = max_liked_segments(n, k, a)
    print(result)