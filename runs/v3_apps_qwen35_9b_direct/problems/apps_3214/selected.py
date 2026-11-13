import sys

def get_core(word):
    # Filter to keep only alphabetic characters and convert to lowercase
    return ''.join(c.lower() for c in word if c.isalpha())

def is_similar(s1, s2):
    # If lengths differ by more than 1, they can't be similar via single edit
    if abs(len(s1) - len(s2)) > 1:
        return False
    
    # Case 1: Same length -> Check for replacement or transpose
    if len(s1) == len(s2):
        diff_count = 0
        diff_indices = []
        for c1, c2 in zip(s1, s2):
            if c1 != c2:
                diff_count += 1
                diff_indices.append((c1, c2))
                if diff_count > 2:
                    return False
        
        if diff_count == 0:
            return False # Must be different words
        
        if diff_count == 1:
            # Replacement
            return True
        
        if diff_count == 2:
            # Check for transpose: two differences must be adjacent swaps
            i, j = diff_indices[0][0], diff_indices[0][1]
            k, l = diff_indices[1][0], diff_indices[1][1]
            # The indices in the string where differences occur
            idx1 = s1.find(i)
            idx2 = s1.find(j)
            # Actually, let's find the positions in s1
            pos1 = s1.find(diff_indices[0][0])
            pos2 = s1.find(diff_indices[1][0])
            
            # Check if positions are adjacent and characters are swapped
            if abs(pos1 - pos2) == 1:
                if (s1[pos1] == diff_indices[1][0] and s1[pos2] == diff_indices[0][0]):
                    return True
            return False
    
    # Case 2: Lengths differ by 1 -> Check for insertion/deletion
    else:
        shorter, longer = (s1, s2) if len(s1) < len(s2) else (s2, s1)
        i = 0
        j = 0
        found_diff = False
        
        while i < len(shorter) and j < len(longer):
            if shorter[i] != longer[j]:
                if found_diff:
                    return False
                found_diff = True
                j += 1 # Skip character in longer string
            else:
                i += 1
                j += 1
        
        return True

def main():
    lines = sys.stdin.read().splitlines()
    
    # Process lines until "***"
    text_lines = []
    for line in lines:
        if line.strip() == "***":
            break
        text_lines.append(line)
    
    # Extract all words and their cores
    words = []
    for line in text_lines:
        # Split by whitespace
        parts = line.split()
        for part in parts:
            core = get_core(part)
            if core: # Must contain at least one alphabetic char
                words.append(core)
    
    # Build a set of unique cores present in the text
    unique_cores = set(words)
    
    # For each unique core, find similarly spelled words
    results = {}
    for core in unique_cores:
        similar_list = []
        for other in unique_cores:
            if core != other and is_similar(core, other):
                similar_list.append(other)
        
        if similar_list:
            similar_list.sort()
            results[core] = similar_list
    
    if not results:
        print("***")
    else:
        for core in sorted(results.keys()):
            print(f"{core}: {' '.join(results[core])}")

if __name__ == "__main__":
    main()