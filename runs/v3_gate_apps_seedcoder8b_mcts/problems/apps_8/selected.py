def min_extra_tiles(tiles):
    from collections import defaultdict

    # Parse the input tiles
    tile_dict = defaultdict(list)
    for tile in tiles:
        number, suit = tile[0], tile[1]
        tile_dict[suit].append(int(number))

    # Function to check if a shuntsu can be formed with the given numbers
    def can_form_shuntsu(numbers):
        numbers = sorted(set(numbers))
        for i in range(len(numbers) - 2):
            if numbers[i] + 1 == numbers[i + 1] and numbers[i + 1] + 1 == numbers[i + 2]:
                return True
        return False

    # Function to check if a koutsu can be formed with the given numbers
    def can_form_koutsu(numbers):
        count = defaultdict(int)
        for number in numbers:
            count[number] += 1
            if count[number] >= 3:
                return True
        return False

    # Check each suit
    for suit, numbers in tile_dict.items():
        if can_form_shuntsu(numbers) or can_form_koutsu(numbers):
            return 0

    # If no koutsu or shuntsu, check if drawing one tile can form either
    for suit, numbers in tile_dict.items():
        unique_numbers = set(numbers)
        for number in range(1, 10):
            if number not in unique_numbers:
                # Check if adding this number forms a shuntsu or koutsu
                potential_numbers = numbers + [number]
                if can_form_shuntsu(potential_numbers) or can_form_koutsu(potential_numbers):
                    return 1

    # If no shuntsu or koutsu can be formed even by drawing one tile
    return 2

# Read input
import sys
input = sys.stdin.read
tiles = input().strip().split()
print(min_extra_tiles(tiles))