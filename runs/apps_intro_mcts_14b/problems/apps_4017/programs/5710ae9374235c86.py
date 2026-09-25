import sys

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    a = list(map(int, data[1:]))
    
    total_sum = sum(a)
    nice_indices = []
    
    for i in range(n):
        if a[i] * 2 == total_sum:
            nice_indices.append(i + 1)
    
    k = len(nice_indices)
    print(k)
    if k > 0:
        print(' '.join(map(str, nice_indices)))

if __name__ == "__main__":
    main()