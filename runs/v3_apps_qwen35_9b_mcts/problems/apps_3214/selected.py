import sys

def get_core(word):
    core = []
    for char in word:
        if char.isalpha():
            core.append(char.lower())
    return ''.join(core)

def is_similar(w1, w2):
    if len(w1) == len(w2):
        if abs(len(w1) - len(w2)) == 0:
            # Same length: check replace or transpose
            if w1 == w2:
                return False
            # Replace
            diff = 0
            for c1, c2 in zip(w1, w2):
                if c1 != c2:
                    diff += 1
                    if diff > 1:
                        return False
            if diff == 1:
                return True
            # Transpose
            if len(w1) >= 2:
                for i in range(len(w1) - 1):
                    if w1[i] == w2[i+1] and w1[i+1] == w2[i]:
                        # Check if swapping i and i+1 in w1 gives w2
                        if w1[:i] + w1[i+1] + w1[i] + w1[i+2:] == w2:
                            return True
            return False
        else:
            return False
    else:
        # Different length: check insert/delete (which is symmetric)
        shorter, longer = (w1, w2) if len(w1) < len(w2) else (w2, w1)
        if len(longer) - len(shorter) != 1:
            return False
        i = 0
        j = 0
        diff = 0
        while i < len(shorter) and j < len(longer):
            if shorter[i] == longer[j]:
                i += 1
                j += 1
            else:
                diff += 1
                if diff > 1:
                    return False
                j += 1
        return True

def solve():
    lines = sys.stdin.read().splitlines()
    cores = set()
    for line in lines:
        if line.strip() == "***":
            break
        words = line.split()
        for w in words:
            core = get_core(w)
            if core:
                cores.add(core)
    
    similar_map = {}
    for core in cores:
        neighbors = []
        for other in cores:
            if core != other and is_similar(core, other):
                neighbors.append(other)
        if neighbors:
            similar_map[core] = sorted(list(set(neighbors)))
    
    if not similar_map:
        print("***")
    else:
        for core in sorted(similar_map.keys()):
            print(f"{core}: {' '.join(similar_map[core])}")

if __name__ == "__main__":
    solve()