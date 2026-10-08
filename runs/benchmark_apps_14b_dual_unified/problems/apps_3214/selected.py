import sys
from collections import defaultdict

def is_similar(word1, word2):
    if abs(len(word1) - len(word2)) > 1:
        return False
    
    if len(word1) == len(word2):
        # Check for replace or transpose
        diff_count = 0
        transpose_possible = False
        for i in range(len(word1)):
            if word1[i] != word2[i]:
                diff_count += 1
                if i < len(word1) - 1 and word1[i] == word2[i + 1] and word1[i + 1] == word2[i]:
                    transpose_possible = True
        return diff_count == 1 or (diff_count == 2 and transpose_possible)
    
    # Assume word1 is shorter than word2
    if len(word1) > len(word2):
        word1, word2 = word2, word1
    
    # Check for insert or delete
    for i in range(len(word1)):
        if word1[i] != word2[i]:
            return word1[i:] == word2[i + 1:] or word1[i + 1:] == word2[i:]
    
    return True

def main():
    input_text = []
    for line in sys.stdin:
        if line.strip() == "***":
            break
        input_text.append(line)
    
    words = []
    for line in input_text:
        words.extend(word.lower() for word in line.split() if any(c.isalpha() for c in word))
    
    word_cores = set()
    for word in words:
        core = ''.join(c for c in word if c.isalpha())
        word_cores.add(core)
    
    similar_words = defaultdict(set)
    for core1 in word_cores:
        for core2 in word_cores:
            if core1 != core2 and is_similar(core1, core2):
                similar_words[core1].add(core2)
                similar_words[core2].add(core1)
    
    if not similar_words:
        print("***")
        return
    
    for core in sorted(similar_words.keys()):
        similar_list = sorted(similar_words[core])
        print(f"{core}: {' '.join(similar_list)}")

if __name__ == "__main__":
    main()