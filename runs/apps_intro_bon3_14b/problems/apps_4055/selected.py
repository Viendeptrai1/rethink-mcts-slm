import sys

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    a = list(map(int, data[1:]))
    
    k = 0
    for i in range(1, n - 1):
        if a[i - 1] == a[i + 1] == 1 and a[i] == 0:
            k += 1
            a[i] = 1  # This line is not necessary for the logic but can be used to mark the flat as checked
    
    print(k)

if __name__ == "__main__":
    main()