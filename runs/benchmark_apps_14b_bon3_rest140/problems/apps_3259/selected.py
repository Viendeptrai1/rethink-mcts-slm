import sys

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    index = 0
    N = int(data[index])
    Q = int(data[index + 1])
    index += 2
    
    boxes = {}
    
    for _ in range(Q):
        query_type = int(data[index])
        if query_type == 1:
            L = int(data[index + 1])
            R = int(data[index + 2])
            A = int(data[index + 3])
            B = int(data[index + 4])
            index += 5
            
            for X in range(L, R + 1):
                boxes[X] = (A * (X - L + 1)) % B
        elif query_type == 2:
            L = int(data[index + 1])
            R = int(data[index + 2])
            index += 3
            
            total_stones = sum(boxes.get(X, 0) for X in range(L, R + 1))
            print(total_stones)

if __name__ == "__main__":
    main()