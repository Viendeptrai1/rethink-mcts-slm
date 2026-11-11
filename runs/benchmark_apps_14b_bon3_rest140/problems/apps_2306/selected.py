import sys

def main():
    import sys
    import math

    def max_distance(N, times, velocities):
        total_time = sum(times)
        max_dist = 0

        for i in range(N):
            t = times[i]
            v = velocities[i]

            # Calculate the maximum distance for each segment
            if t <= v:
                # If time is less than or equal to velocity, it can accelerate to v and then decelerate back to 0
                dist = (v * v) / 2
            else:
                # If time is more than velocity, it can accelerate to v, maintain at v, and then decelerate back to 0
                accelerate_time = v
                maintain_time = t - 2 * v
                if maintain_time < 0:
                    # Not enough time to reach full speed, so it accelerates and then decelerates
                    accelerate_time = t / 2
                    maintain_time = 0
                dist = (accelerate_time * accelerate_time) / 2 + v * maintain_time + (accelerate_time * accelerate_time) / 2

            max_dist += dist

        return max_dist

    # Read input
    N = int(sys.stdin.readline().strip())
    times = list(map(int, sys.stdin.readline().strip().split()))
    velocities = list(map(int, sys.stdin.readline().strip().split()))

    # Calculate and print the maximum distance
    result = max_distance(N, times, velocities)
    print(f"{result:.15f}")

if __name__ == "__main__":
    main()