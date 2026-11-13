def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    a = list(map(int, data[1:n+1]))
    
    a_with_index = sorted((value, index) for index, value in enumerate(a))
    
    b = [0] * n
    next_rating = 1
    
    for value, index in a_with_index:
        b[index] = max(value, next_rating)
        next_rating += 1
    
    print(" ".join(map(str, b)))

if __name__ == "__main__":
    main()