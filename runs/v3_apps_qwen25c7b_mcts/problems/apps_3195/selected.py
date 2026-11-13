from typing import List

def traffic_light_probability(Tg: int, Ty: int, Tr: int, n: int, observations: List[List[int]], tq: int, cq: str) -> float:
    total_cycle = Tg + Ty + Tr
    current_state = None
    start_time = None
    
    for t, color in observations:
        if current_state is None:
            current_state = color
            start_time = t
        else:
            if current_state == 'green':
                if color == 'yellow':
                    expected_t = start_time + Tg
                elif color == 'red':
                    expected_t = start_time + Tg + Ty
            elif current_state == 'yellow':
                if color == 'red':
                    expected_t = start_time + Tg + Ty
                elif color == 'green':
                    expected_t = start_time + Tg + Ty + Tr
            elif current_state == 'red':
                if color == 'green':
                    expected_t = start_time + Tg + Ty + Tr
            
            if abs(t - expected_t) < 1e-3:
                current_state = color
            else:
                break
    
    if current_state is None:
        return 0.0
    
    if cq == 'green':
        return (tq - start_time) % total_cycle / total_cycle
    elif cq == 'yellow':
        return (tq - start_time - Tg) % total_cycle / total_cycle
    elif cq == 'red':
        return (tq - start_time - Tg - Ty) % total_cycle / total_cycle

# Example usage:
if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    
    Tg = int(data[0])
    Ty = int(data[1])
    Tr = int(data[2])
    n = int(data[3])
    
    observations = []
    index = 4
    for _ in range(n):
        t = int(data[index])
        color = data[index + 1]
        observations.append([t, color])
        index += 2
    
    tq = int(data[index])
    cq = data[index + 1]
    
    result = traffic_light_probability(Tg, Ty, Tr, n, observations, tq, cq)
    print(result)