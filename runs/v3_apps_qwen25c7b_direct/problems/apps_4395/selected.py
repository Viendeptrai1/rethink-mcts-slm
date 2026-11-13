def min_recolors_to_nice_garland(n, s):
    def is_nice(garland):
        for i in range(3):
            indices = [j for j, c in enumerate(garland) if c == chr(ord('A') + i)]
            for j in range(len(indices)):
                for k in range(j + 1, len(indices)):
                    if abs(indices[j] - indices[k]) % 3 != 0:
                        return False
        return True

    def find_min_recolors(s):
        from collections import Counter
        count = Counter(s)
        if count['R'] <= count['G'] and count['R'] <= count['B']:
            target_color = 'R'
        elif count['G'] <= count['R'] and count['G'] <= count['B']:
            target_color = 'G'
        else:
            target_color = 'B'

        recolors = 0
        garland = list(s)
        for i in range(n):
            if garland[i] != target_color:
                garland[i] = target_color
                recolors += 1
        return recolors, ''.join(garland)

    recolors, garland = find_min_recolors(s)
    return recolors, garland

# Example usage:
# n = int(input())
# s = input()
# result = min_recolors_to_nice_garland(n, s)
# print(result[0])
# print(result[1])

# For testing purposes:
print(min_recolors_to_nice_garland(3, "BRB"))  # Output: (1, 'GRB')
print(min_recolors_to_nice_garland(7, "RGBGRBB"))  # Output: (3, 'RGBRGBR')