import sys

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    
    n = int(data[0])
    m = int(data[1])
    
    exams = []
    index = 2
    for _ in range(m):
        s_i = int(data[index])
        d_i = int(data[index + 1])
        c_i = int(data[index + 2])
        exams.append((s_i, d_i, c_i))
        index += 3
    
    # Check if it's possible to prepare for all exams
    total_prep_days_needed = sum(c_i for _, _, c_i in exams)
    total_days_available = sum(d_i - s_i for s_i, d_i, _ in exams)
    
    if total_prep_days_needed > total_days_available:
        print(-1)
        return
    
    # Initialize the schedule
    schedule = [0] * n
    
    # Try to assign preparation days
    for i in range(m):
        s_i, d_i, c_i = exams[i]
        prep_days = 0
        for j in range(s_i, d_i):
            if schedule[j - 1] == 0:
                schedule[j - 1] = i + 1
                prep_days += 1
                if prep_days == c_i:
                    break
    
    # Assign exam days
    for i in range(m):
        s_i, d_i, _ = exams[i]
        schedule[d_i - 1] = m + 1
    
    # Check if all exams are prepared for
    for i in range(m):
        s_i, d_i, c_i = exams[i]
        prep_days = sum(1 for j in range(s_i, d_i) if schedule[j - 1] == i + 1)
        if prep_days != c_i:
            print(-1)
            return
    
    # Print the schedule
    print(" ".join(map(str, schedule)))

if __name__ == "__main__":
    main()