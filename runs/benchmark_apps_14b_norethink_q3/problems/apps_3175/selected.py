import math
import random

def is_valid_polygon(sides):
    sides.sort()
    return sum(sides[:-1]) > sides[-1]

def polygon_area(sides):
    n = len(sides)
    if n < 3:
        return 0
    # Using Brahmagupta's formula for cyclic quadrilaterals as an approximation
    if n == 4:
        a, b, c, d = sides
        s = (a + b + c + d) / 2
        return math.sqrt((s - a) * (s - b) * (s - c) * (s - d))
    # For other polygons, approximate using the average side length
    perimeter = sum(sides)
    avg_side = perimeter / n
    return (avg_side ** 2) * (n / (4 * math.tan(math.pi / n)))

def simulated_annealing(sides, max_iterations=10000, initial_temp=1000, cooling_rate=0.99):
    current_sides = random.sample(sides, min(len(sides), 4))
    while not is_valid_polygon(current_sides):
        current_sides = random.sample(sides, min(len(sides), 4))
    current_area = polygon_area(current_sides)
    
    best_sides = current_sides[:]
    best_area = current_area
    
    temperature = initial_temp
    
    for _ in range(max_iterations):
        new_sides = current_sides[:]
        index = random.randint(0, len(new_sides) - 1)
        new_sides[index] = random.choice(sides)
        
        if is_valid_polygon(new_sides):
            new_area = polygon_area(new_sides)
            delta = new_area - current_area
            
            if delta > 0 or random.random() < math.exp(delta / temperature):
                current_sides = new_sides[:]
                current_area = new_area
                
                if current_area > best_area:
                    best_sides = current_sides[:]
                    best_area = current_area
        
        temperature *= cooling_rate
    
    return best_area

def main():
    import sys
    input = sys.stdin.read
    data = input().split()
    n = int(data[0])
    sides = list(map(int, data[1:]))
    
    max_area = simulated_annealing(sides)
    print(f"{max_area:.3f}")

if __name__ == "__main__":
    main()