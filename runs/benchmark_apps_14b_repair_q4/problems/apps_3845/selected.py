import sys

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    A = int(data[0])
    B = int(data[1])
    
    h = A + B
    w = 1
    
    print(h, w)
    
    for i in range(h):
        if i < A:
            print(".")
        else:
            print("#")

if __name__ == "__main__":
    main()