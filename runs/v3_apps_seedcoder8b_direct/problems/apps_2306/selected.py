def max_distance():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    t = list(map(int, data[1:N+1]))
    v = list(map(int, data[N+1:2*N+1]))
    
    max_distance = 0.0
    
    for i in range(N):
        # Calculate the distance covered in the i-th segment
        # The distance covered in the i-th segment is given by the integral of the velocity over time
        # Distance = (v_i * t_i) + (1/2) * a * t_i^2
        # Since the acceleration is ±1 m/s^2, we need to consider both cases
        # For acceleration a = 1 m/s^2
        distance_accelerate = (v[i] * t[i]) + (0.5 * 1 * t[i]**2)
        # For acceleration a = -1 m/s^2
        distance_decelerate = (v[i] * t[i]) + (0.5 * (-1) * t[i]**2)
        
        # The maximum distance for this segment is the maximum of the two cases
        max_distance += max(distance_accelerate, distance_decelerate)
    
    print(max_distance)