import sys
from collections import defaultdict

def get_core(word):
    return ''.join(filter(str.isalpha, word)).lower()

def are_similar(core1, core2):
    if core1 == core2:
        return False
    len1, len2 = len(core1), len(core2)
    if abs(len1 - len2) > 1:
        return False
    
    if len1 == len2:
        # Check for single replacement
        diff_count = sum(1 for a, b in zip(core1, core2) if a != b)
        return diff_count == 1
    elif len1 < len2:
        # Check for single insertion
        for i in range(len2):
            if core1 == core2[:i] + core2[i+1:]:
                return True
    else:
        # Check for single deletion
        for i in range(len1):
            if core1[:i] + core1[i+1:] == core2:
                return True
    return False

def transpose(core):
    for i in range(len(core) - 1):
        if core[i] != core[i + 1]:
            swapped = core[:i] + core[i + 1] + core[i] + core[i + 2:]
            yield swapped

def find_similar_words(text):
    words = text.split()
    cores = [get_core(word) for word in words]
    similar_dict = defaultdict(set)
    
    for i, core in enumerate(cores):
        for j, other_core in enumerate(cores):
            if i != j and are_similar(core, other_core):
                similar_dict[core].add(other_core)
        # Check for transpositions
        for transposed_core in transpose(core):
            if transposed_core in cores:
                similar_dict[core].add(transposed_core)
    
    result = []
    for core in sorted(similar_dict.keys()):
        if similar_dict[core]:
            similar_list = sorted(similar_dict[core])
            result.append(f"{core}: {' '.join(similar_list)}")
    
    return result

def main():
    input_lines = sys.stdin.read().strip().split('\n')
    text = '\n'.join(input_lines[:-1])  # Exclude the end marker "***"
    similar_words = find_similar_words(text)
    if similar_words:
        for line in similar_words:
            print(line)
    else:
        print("***")

if __name__ == "__main__":
    main()