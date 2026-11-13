def count_equal_arc_abc_choices():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    difficulties = list(map(int, data[1:]))
    
    difficulties.sort()
    
    count = 0
    for i in range(N // 2):
        if difficulties[i] < difficulties[N - 1 - i]:
            count += 1
    
    print(count)