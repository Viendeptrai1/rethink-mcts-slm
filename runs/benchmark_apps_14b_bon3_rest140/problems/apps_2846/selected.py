import sys

def calculate_h_index(citations):
    citations.sort(reverse=True)
    h_index = 0
    for i, citation in enumerate(citations):
        if citation >= i + 1:
            h_index = i + 1
        else:
            break
    return h_index

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    citations = list(map(int, data[1:]))
    
    h_index = calculate_h_index(citations)
    print(h_index)

if __name__ == "__main__":
    main()