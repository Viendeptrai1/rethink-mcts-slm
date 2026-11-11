import sys

def main():
    import sys
    import bisect
    
    def count_valid_ks(N, difficulties):
        difficulties.sort()
        count = 0
        for i in range(N // 2):
            k = difficulties[i + N // 2]
            count += N // 2 == bisect.bisect_left(difficulties, k)
        return count
    
    N = int(sys.stdin.readline())
    difficulties = list(map(int, sys.stdin.readline().split()))
    print(count_valid_ks(N, difficulties))

if __name__ == "__main__":
    main()