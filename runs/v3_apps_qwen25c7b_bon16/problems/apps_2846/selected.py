def h_index(citations):
    citations.sort(reverse=True)
    h = 0
    for i in range(len(citations)):
        if citations[i] >= i + 1:
            h = i + 1
        else:
            break
    return h

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    n = int(data[0])
    citations = list(map(int, data[1:]))
    print(h_index(citations))