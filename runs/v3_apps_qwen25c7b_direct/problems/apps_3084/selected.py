from sys import stdin, stdout

def get_next_time(current):
    h, m = map(int, current.split(':'))
    next_times = {current}
    
    def valid_time(h, m):
        return 0 <= h < 24 and 0 <= m < 60
    
    def increment(digit):
        return (digit + 1) % 10
    
    def decrement(digit):
        return (digit - 1) % 10
    
    queue = [(h, m)]
    visited = set()
    
    while queue:
        h, m = queue.pop(0)
        if (h, m) in visited:
            continue
        visited.add((h, m))
        
        for i in range(4):
            new_h, new_m = h, m
            if i < 2:
                new_h = list(str(new_h))
                new_h[i] = str(increment(int(new_h[i])))
                new_h = int(''.join(new_h))
            else:
                new_m = list(str(new_m))
                new_m[i-2] = str(increment(int(new_m[i-2])))
                new_m = int(''.join(new_m))
            
            if valid_time(new_h, new_m):
                next_times.add(f"{new_h:02}:{new_m:02}")
                queue.append((new_h, new_m))
                
            new_h, new_m = h, m
            if i < 2:
                new_h = list(str(new_h))
                new_h[i] = str(decrement(int(new_h[i])))
                new_h = int(''.join(new_h))
            else:
                new_m = list(str(new_m))
                new_m[i-2] = str(decrement(int(new_m[i-2])))
                new_m = int(''.join(new_m))
            
            if valid_time(new_h, new_m):
                next_times.add(f"{new_h:02}:{new_m:02}")
                queue.append((new_h, new_m))
    
    return sorted(next_times)

def main():
    current = stdin.readline().strip()
    target = stdin.readline().strip()
    
    times = get_next_time(current)
    times.remove(target)
    times.add(current)
    times.add(target)
    
    stdout.write(f"{len(times)}\n")
    for time in times:
        stdout.write(time + '\n')

if __name__ == "__main__":
    main()