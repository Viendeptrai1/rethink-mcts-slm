def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    a = list(map(int, data[1:]))
    
    a.sort()
    
    first_half = a[:n]
    second_half = a[n:]
    
    # Check if swapping two smallest elements can make the sums unequal
    if sum(first_half) != sum(second_half):
        print(*a)
        return
    
    # Attempt to swap elements to make sums unequal
    for i in range(n):
        for j in range(n):
            if i != j:
                first_half[i], second_half[j] = second_half[j], first_half[i]
                
                if sum(first_half) != sum(second_half):
                    print(*(first_half + second_half))
                    return
                
                # Swap back to continue checking
                first_half[i], second_half[j] = second_half[j], first_half[i]
    
    print(-1)

if __name__ == "__main__":
    main()