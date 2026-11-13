def calculate_h_index(n, citations):
    citations.sort(reverse=True)
    h_index = 0
    for i, c in enumerate(citations):
        if c >= i + 1:
            h_index = i + 1
        else:
            break
    return h_index

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    citations = list(map(int, data[1:n+1]))
    
    result = calculate_h_index(n, citations)
    print(result)