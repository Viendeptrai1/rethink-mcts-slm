import sys

def f(x):
    x += 1
    while x % 10 == 0:
        x //= 10
    return x

def count_reachable_numbers(n):
    reachable = set()
    queue = [n]
    
    while queue:
        current = queue.pop(0)
        if current not in reachable:
            reachable.add(current)
            next_number = f(current)
            if next_number not in reachable:
                queue.append(next_number)
    
    return len(reachable)

def main():
    import sys
    n = int(sys.stdin.read().strip())
    print(count_reachable_numbers(n))

if __name__ == "__main__":
    main()