def max_path_length(v_1, v_2, t, d):
    speeds = [v_1] * t
    speeds[0] = v_1
    speeds[-1] = v_2
    
    for i in range(1, t):
        if speeds[i] < v_2:
            speeds[i] = min(v_2, speeds[i-1] + d)
        else:
            speeds[i] = max(v_2, speeds[i-1] - d)
    
    total_distance = sum(speeds)
    return total_distance

if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().strip().split()
    v_1 = int(data[0])
    v_2 = int(data[1])
    t = int(data[2])
    d = int(data[3])
    
    result = max_path_length(v_1, v_2, t, d)
    print(result)