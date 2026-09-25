import sys

def count_reachable_numbers(n):
    reachable = set()
    current = n
    
    while current not in reachable:
        reachable.add(current)
        current += 1
        while current % 10 == 0:
            current //= 10
    
    return len(reachable)

def main():
    import sys
    n = int(sys.stdin.read().strip())
    print(count_reachable_numbers(n))

if __name__ == "__main__":
    main()