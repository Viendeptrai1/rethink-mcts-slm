def find_nearest_checkpoints():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    M = int(data[1])
    
    students = []
    checkpoints = []
    
    index = 2
    for _ in range(N):
        a_i = int(data[index])
        b_i = int(data[index + 1])
        students.append((a_i, b_i))
        index += 2
    
    for _ in range(M):
        c_j = int(data[index])
        d_j = int(data[index + 1])
        checkpoints.append((c_j, d_j))
        index += 2
    
    results = []
    
    for student in students:
        min_distance = float('inf')
        nearest_checkpoint = -1
        for j, checkpoint in enumerate(checkpoints):
            distance = abs(student[0] - checkpoint[0]) + abs(student[1] - checkpoint[1])
            if distance < min_distance:
                min_distance = distance
                nearest_checkpoint = j + 1
        results.append(nearest_checkpoint)
    
    for result in results:
        print(result)

find_nearest_checkpoints()