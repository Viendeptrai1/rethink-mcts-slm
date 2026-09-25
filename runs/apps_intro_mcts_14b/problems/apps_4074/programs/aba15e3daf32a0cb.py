import sys

def main():
    import sys
    import math
    
    def read_ints():
        return map(int, sys.stdin.readline().split())
    
    t = int(sys.stdin.readline())
    results = []
    
    for _ in range(t):
        n, k = read_ints()
        package_size = min(n, k)
        num_packages = math.ceil(n / package_size)
        results.append(num_packages)
    
    for result in results:
        print(result)

if __name__ == "__main__":
    main()