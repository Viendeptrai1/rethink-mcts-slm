import sys

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    exams = []
    
    index = 1
    for _ in range(n):
        a_i = int(data[index])
        b_i = int(data[index + 1])
        exams.append((a_i, b_i))
        index += 2
    
    exams.sort(key=lambda x: x[0])
    
    current_day = 0
    for a_i, b_i in exams:
        if b_i > current_day:
            current_day = b_i
        else:
            current_day = a_i
    
    print(current_day)

if __name__ == "__main__":
    main()