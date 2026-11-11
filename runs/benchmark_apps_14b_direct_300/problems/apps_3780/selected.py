import sys
import math

def main():
    import sys
    import math

    def read_ints():
        return map(int, sys.stdin.readline().split())

    x1, y1, x2, y2 = read_ints()
    vmax, t = read_ints()
    vx1, vy1 = read_ints()
    vx2, vy2 = read_ints()

    def distance(x1, y1, x2, y2):
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    def time_to_travel(x1, y1, x2, y2, vx, vy, vmax):
        dx = x2 - x1
        dy = y2 - y1
        d = distance(x1, y1, x2, y2)
        if d == 0:
            return 0
        # Relative velocity components
        ux = vx
        uy = vy
        # Effective velocity components
        ex = vmax * (dx / d) - ux
        ey = vmax * (dy / d) - uy
        # Effective speed
        es = math.sqrt(ex ** 2 + ey ** 2)
        if es == 0:
            return float('inf')
        return d / es

    # Calculate time to travel in the first t seconds
    time1 = time_to_travel(x1, y1, x1 + vx1 * t, y1 + vy1 * t, vx1, vy1, vmax)
    # Calculate time to travel in the remaining time
    time2 = time_to_travel(x1 + vx1 * t, y1 + vy1 * t, x2, y2, vx2, vy2, vmax)
    total_time = time1 + time2
    print(total_time)

if __name__ == "__main__":
    main()