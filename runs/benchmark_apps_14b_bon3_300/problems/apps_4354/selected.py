import sys

def manhattan_distance(x1, y1, x2, y2):
    return abs(x1 - x2) + abs(y1 - y2)

def find_nearest_checkpoint(N, M, students, checkpoints):
    result = []
    for i in range(N):
        min_distance = float('inf')
        nearest_checkpoint = -1
        for j in range(M):
            distance = manhattan_distance(students[i][0], students[i][1], checkpoints[j][0], checkpoints[j][1])
            if distance < min_distance:
                min_distance = distance
                nearest_checkpoint = j + 1
        result.append(nearest_checkpoint)
    return result

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    N = int(data[0])
    M = int(data[1])
    
    index = 2
    students = []
    for _ in range(N):
        a = int(data[index])
        b = int(data[index + 1])
        students.append((a, b))
        index += 2
    
    checkpoints = []
    for _ in range(M):
        c = int(data[index])
        d = int(data[index + 1])
        checkpoints.append((c, d))
        index += 2
    
    result = find_nearest_checkpoint(N, M, students, checkpoints)
    for checkpoint in result:
        print(checkpoint)

if __name__ == "__main__":
    main()