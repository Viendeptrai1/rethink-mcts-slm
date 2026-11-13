import sys

def find_nearest_checkpoint(N, M, students, checkpoints):
    result = []
    for student in students:
        min_distance = float('inf')
        nearest_checkpoint = -1
        for j in range(M):
            distance = abs(student[0] - checkpoints[j][0]) + abs(student[1] - checkpoints[j][1])
            if distance < min_distance or (distance == min_distance and j < nearest_checkpoint):
                min_distance = distance
                nearest_checkpoint = j + 1
        result.append(nearest_checkpoint)
    return result

if __name__ == "__main__":
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    M = int(data[1])
    
    students = [(int(data[2 + 2 * i]), int(data[3 + 2 * i])) for i in range(N)]
    checkpoints = [(int(data[2 + 2 * N + 2 * i]), int(data[3 + 2 * N + 2 * i])) for i in range(M)]
    
    result = find_nearest_checkpoint(N, M, students, checkpoints)
    
    for r in result:
        print(r)