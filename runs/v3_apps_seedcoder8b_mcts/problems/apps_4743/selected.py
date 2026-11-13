def nimionese_translation(sentence):
    hard_consonants = 'bcdfgkntp'
    nearest_consonant = {'b': 'p', 'c': 'k', 'd': 't', 'g': 'k', 'k': 'g', 'n': 't', 'p': 'b', 't': 'd'}
    nearest_vowel = {'a': 'ah', 'o': 'oh', 'u': 'uh'}

    def convert_word(word):
        if not word:
            return word

        # Handle the first letter
        first_letter = word[0].lower()
        if first_letter in hard_consonants:
            word = nearest_consonant[first_letter] + word[1:]
        else:
            word = word

        # Handle subsequent hard consonants
        for i in range(1, len(word)):
            if word[i].lower() in hard_consonants:
                if word[i].lower() == first_letter:
                    word = word[:i] + word[i] + word[i+1:]
                else:
                    word = word[:i] + nearest_consonant[first_letter] + word[i+1:]

        # Handle "hip-po" to "gip-go"
        word = word.replace('hip', 'gip').replace('po', 'go')

        # Handle "dog" to "dogah"
        word = word.replace('dog', 'dogah')

        # Handle "hip" to "gipoh"
        word = word.replace('hip', 'gipoh')

        # Handle ending with hard consonant
        last_letter = word[-1].lower()
        if last_letter in hard_consonants:
            nearest_end = min(nearest_vowel.keys(), key=lambda x: abs(ord(x) - ord(last_letter)))
            word += nearest_vowel[nearest_end]

        return word

    words = sentence.split()
    translated_words = [convert_word(word) for word in words]
    return ' '.join(translated_words)

if __name__ == "__main__":
    import sys
    input_sentence = sys.stdin.read().strip()
    print(nimionese_translation(input_sentence))