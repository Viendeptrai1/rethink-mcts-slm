def min_recolors_to_nice_garland(n, s):
    def is_nice(garland):
        for i in range(3):
            indices = [j for j, c in enumerate(garland) if c == chr(ord('A') + i)]
            for j in range(len(indices)):
                for k in range(j + 1, len(indices)):
                    if abs(indices[j] - indices[k]) % 3 != 0:
                        return False
        return True

    def get_min_recolors_and_garland(s):
        min_recolors = float('inf')
        best_garland = ""
        for pattern in ['RGB', 'RBG', 'GRB', 'GBR', 'BRG', 'BGR']:
            garland = list(s)
            recolors = 0
            for i in range(n):
                if garland[i] != pattern[i % 3]:
                    garland[i] = pattern[i % 3]
                    recolors += 1
            if is_nice("".join(garland)):
                if recolors < min_recolors:
                    min_recolors = recolors
                    best_garland = "".join(garland)
        return min_recolors, best_garland

    min_recolors, best_garland = get_min_recolors_and_garland(s)
    return min_recolors, best_garland

# Example usage:
if __name__ == "__main__":
    import sys
    input = sys.stdin.read
    data = input().split()
    n = int(data[0])
    s = data[1]
    result = min_recolors_to_nice_garland(n, s)
    print(result[0])
    print(result[1])