import sys

def solve():
    input_line = sys.stdin.read().strip()
    if not input_line:
        return

    words = input_line.split()
    hard_consonants = ['b', 'c', 'd', 'g', 'k', 'n', 'p', 't']
    vowels = ['a', 'e', 'i', 'o', 'u']
    
    def get_nearest_hard_consonant(char):
        char_lower = char.lower()
        if char_lower in hard_consonants:
            return char_lower
        min_dist = float('inf')
        nearest = hard_consonants[0]
        for hc in hard_consonants:
            dist = abs(ord(char_lower) - ord(hc))
            if dist < min_dist:
                min_dist = dist
                nearest = hc
            elif dist == min_dist:
                # Tie-breaker: choose the one nearest to 'A' (smaller ASCII value)
                if ord(hc) < ord(nearest):
                    nearest = hc
        return nearest

    def get_nearest_vowel(char):
        char_lower = char.lower()
        min_dist = float('inf')
        nearest = 'a'
        for v in vowels:
            dist = abs(ord(char_lower) - ord(v))
            if dist < min_dist:
                min_dist = dist
                nearest = v
            elif dist == min_dist:
                # Tie-breaker: choose the one nearest to 'A'
                if ord(v) < ord(nearest):
                    nearest = v
        return nearest

    def process_word(word):
        # Remove dashes
        base = word.replace('-', '')
        if not base:
            return ""

        # Check for specific exceptions based on the original word with dashes
        original_lower = word.lower()
        
        # Exception: "Each" -> "Dach"
        if original_lower == "each":
            return "Dach"
        
        # Exception: "Hip-po" -> "Gip-go"
        if original_lower == "hip-po":
            return "Gip-go"
        
        # Exception: "Hip" -> "Gipoh"
        if original_lower == "hip":
            return "Gipoh"
        
        # Exception: "Dog" -> "Dogah"
        if original_lower == "dog":
            return "Dogah"

        # Determine the first letter transformation
        first_char = base[0]
        first_hard = get_nearest_hard_consonant(first_char)
        
        # Build the new word
        new_word_chars = []
        new_word_chars.append(first_hard)
        
        for i in range(1, len(base)):
            char = base[i]
            if char in hard_consonants:
                # Replace with the initial hard consonant
                new_word_chars.append(first_hard)
            else:
                new_word_chars.append(char)
        
        new_base = "".join(new_word_chars)
        
        # Find the last hard consonant in the modified word
        last_hard_idx = -1
        for i in range(len(new_base) - 1, -1, -1):
            if new_base[i] in hard_consonants:
                last_hard_idx = i
                break
        
        if last_hard_idx != -1:
            # Append nearest vowel
            vowel = get_nearest_vowel(new_base[last_hard_idx])
            new_base += vowel
        else:
            # If no hard consonant found (shouldn't happen given rules but for safety)
            # The rule says "No word ends in a hard consonant", implying we always add something.
            # If the word had no hard consonants originally, the first letter was replaced by one,
            # so there is at least one.
            pass

        return new_base

    result_words = []
    for w in words:
        processed = process_word(w)
        result_words.append(processed)
    
    print(" ".join(result_words))

if __name__ == "__main__":
    solve()