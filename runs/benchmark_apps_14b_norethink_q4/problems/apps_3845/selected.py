import sys

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    A = int(data[0])
    B = int(data[1])
    
    h = A + 1
    w = B + 1
    
    print(h, w)
    
    for i in range(h):
        row = []
        for j in range(w):
            if i < A:
                if (i + j) % 2 == 0:
                    row.append('.')
                else:
                    row.append('#')
            else:
                if (i + j) % 2 == 0:
                    row.append('#')
                else:
                    row.append('.')
        print(''.join(row))

if __name__ == "__main__":
    main()