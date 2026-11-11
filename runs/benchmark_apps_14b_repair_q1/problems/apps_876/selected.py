import sys

def find_minimum_i(n, k, A):
    def p(x):
        return [0] + [sum(x[:i]) for i in range(1, len(x) + 1)]
    
    current_A = A
    i = 0
    while True:
        if any(y >= k for y in current_A):
            return i
        current_A = p([x - 1 for x in current_A])
        i += 1

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    k = int(data[1])
    A = list(map(int, data[2:2+n]))
    
    result = find_minimum_i(n, k, A)
    print(result)

if __name__ == "__main__":
    main()