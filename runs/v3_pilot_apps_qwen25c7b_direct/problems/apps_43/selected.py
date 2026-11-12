import sys
from math import atan2, pi

def read_input():
    input = sys.stdin.read
    data = input().split()
    n = int(data[0])
    vectors = [(int(data[2*i+1]), int(data[2*i+2])) for i in range(n)]
    return n, vectors

def find_min_angle_pair(vectors):
    min_angle = float('inf')
    min_pair = (-1, -1)
    
    for i in range(len(vectors)):
        for j in range(i + 1, len(vectors)):
            dx1, dy1 = vectors[i]
            dx2, dy2 = vectors[j]
            
            # Calculate the angle using atan2 for non-oriented angle calculation
            angle = abs(atan2(dy1 * dx2 - dx1 * dy2, dx1 * dx2 + dy1 * dy2))
            if angle > pi:
                angle = 2 * pi - angle
            
            if angle < min_angle:
                min_angle = angle
                min_pair = (i + 1, j + 1)
    
    return min_pair

def main():
    n, vectors = read_input()
    result = find_min_angle_pair(vectors)
    print(result[0], result[1])

if __name__ == "__main__":
    main()