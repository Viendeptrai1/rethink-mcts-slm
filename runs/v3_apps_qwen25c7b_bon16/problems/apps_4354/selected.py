import sys

def main():
    input = sys.stdin.read
    data = input().split()
    
    index = 0
    N = int(data[index])
    M = int(data[index + 1])
    index += 2
    
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
    
    results = []
    for student in students:
        min_distance = float('inf')
        closest_checkpoint_index = -1
        for i, checkpoint in enumerate(checkpoints):
            distance = abs(student[0] - checkpoint[0]) + abs(student[1] - checkpoint[1])
            if distance < min_distance or (distance == min_distance and i < closest_checkpoint_index):
                min_distance = distance
                closest_checkpoint_index = i + 1
        results.append(closest_checkpoint_index)
    
    for result in results:
        print(result)

if __name__ == "__main__":
    main()