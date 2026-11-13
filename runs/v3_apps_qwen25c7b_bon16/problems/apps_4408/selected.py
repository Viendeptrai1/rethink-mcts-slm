import sys
input = sys.stdin.read
data = input().split()

def main():
    n = int(data[0])
    k = int(data[1])
    cards = list(map(int, data[2:2+3*n]))
    favorites = list(map(int, data[2+3*n:2+3*n+n]))
    joy_levels = list(map(int, data[2+3*n+n:]))

    count = [0] * (max(cards) + 1)
    for card in cards:
        count[card] += 1

    favorite_counts = []
    for favorite in favorites:
        favorite_counts.append(count[favorite])

    favorite_counts.sort(reverse=True)
    total_joy_level = sum(h * min(t, k) for h, t in zip(joy_levels, favorite_counts))
    print(total_joy_level)

if __name__ == "__main__":
    main()