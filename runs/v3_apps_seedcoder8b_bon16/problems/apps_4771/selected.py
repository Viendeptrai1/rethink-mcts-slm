def main():
    n, V = map(int, input().split())
    max_difference = float('-inf')
    
    for _ in range(n):
        l, w, h = map(int, input().split())
        volume = l * w * h
        difference = volume - V
        max_difference = max(max_difference, difference)
    
    print(max_difference)

if __name__ == "__main__":
    main()