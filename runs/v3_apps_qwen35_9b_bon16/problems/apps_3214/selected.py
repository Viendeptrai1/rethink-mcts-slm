import sys

def get_core(word):
    # Filter: keep only alphabetic characters, convert to lowercase
    core = ''.join(c.lower() for c in word if c.isalpha())
    return core if core else None

def is_similar(a, b):
    if a == b:
        return False
    len_a = len(a)
    len_b = len(b)
    diff = abs(len_a - len_b)
    if diff > 1:
        return False
    # Try to match with at most one edit distance
    if len_a == len_b:
        # Replacement or Transpose
        diffs = 0
        for i in range(len_a):
            if a[i] != b[i]:
                diffs += 1
                if diffs > 1:
                    break
        if diffs == 1:
            return True
        # Check for transpose (adjacent swap)
        if diffs == 0:
            return False
        # Check if exactly two adjacent chars are swapped
        for i in range(len_a - 1):
            if a[i] == b[i+1] and a[i+1] == b[i]:
                # Check rest matches
                match = True
                for k in range(len_a):
                    if k == i or k == i+1:
                        continue
                    if a[k] != b[k]:
                        match = False
                        break
                if match:
                    return True
        return False
    else:
        # Insertion/Deletion
        shorter, longer = (a, b) if len_a < len_b else (b, a)
        s_len, l_len = len(shorter), len(longer)
        i = 0
        j = 0
        edits = 0
        while i < s_len and j < l_len:
            if shorter[i] == longer[j]:
                i += 1
                j += 1
            else:
                edits += 1
                if edits > 1:
                    return False
                j += 1
        return True

def main():
    lines = sys.stdin.read().splitlines()
    text_lines = []
    for line in lines:
        if line.strip() == "***":
            break
        text_lines.append(line)

    full_text = ' '.join(text_lines)
    
    # Tokenize
    words = []
    current = []
    for ch in full_text:
        if ch.isspace():
            if current:
                words.append(''.join(current))
                current = []
        else:
            current.append(ch)
    if current:
        words.append(''.join(current))

    cores = {} # map original word -> list of cores? No, we need to process each word's core
    # Actually, we need to find all (core, similar_cores) pairs from the text.
    # Step 1: Extract all cores from the text.
    # Step 2: For each unique core found, find all other unique cores in the text that are similar.
    
    all_cores = []
    for w in words:
        c = get_core(w)
        if c:
            all_cores.append(c)
    
    unique_cores = sorted(list(set(all_cores)))
    
    results = {}
    
    for i, core in enumerate(unique_cores):
        similar_list = []
        for j, other in enumerate(unique_cores):
            if i == j:
                continue
            if is_similar(core, other):
                similar_list.append(other)
        if similar_list:
            similar_list.sort()
            results[core] = similar_list

    if not results:
        print("***")
    else:
        for core in sorted(results.keys()):
            similar = results[core]
            print(f"{core}: {' '.join(similar)}")

if __name__ == "__main__":
    main()