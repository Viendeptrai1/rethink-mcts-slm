import sys

def main():
    import sys
    import bisect
    
    def solve(N, difficulties):
        difficulties.sort()
        count = 0
        target = N // 2
        
        for i in range(N):
            if difficulties[i] >= difficulties[target]:
                count += 1
        
        return count
    
    N = int(sys.stdin.readline().strip())
    difficulties = list(map(int, sys.stdin.readline().strip().split()))
    
    result = solve(N, difficulties)
    print(result)

if __name__ == "__main__":
    main()