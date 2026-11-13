def translate_to_nimionese(sentence):
    vowels = 'aeiou'
    hard_consonants = 'bcdfgknpst'

    def replace_first_consonant(word):
        if not word:
            return word
        first_char = word[0]
        if first_char.lower() in hard_consonants:
            index = hard_consonants.find(first_char.lower())
            new_char = hard_consonants[(index + 1) % len(hard_consonants)]
            return new_char.upper() + word[1:]
        else:
            return word

    def replace_each_with_dach(word):
        return 'Dach' if word.lower() == 'each' else word

    def replace_hard_consonants(word):
        result = []
        for i, char in enumerate(word):
            if char.lower() in hard_consonants:
                if i == 0:
                    result.append(replace_first_consonant(char))
                else:
                    result.append(char)
            else:
                result.append(char)
        return ''.join(result)

    def add_ending_vowel(word):
        if not word:
            return word
        last_char = word[-1].lower()
        if last_char in hard_consonants:
            index = hard_consonants.find(last_char)
            new_char = hard_consonants[index // 2]
            return word[:-1] + new_char + 'aou'[index // 2]
        else:
            return word

    words = sentence.split(' ')
    translated_words = []

    for word in words:
        word = replace_each_with_dach(word)
        word = replace_hard_consonants(word)
        word = add_ending_vowel(word)
        translated_words.append(word)

    return ' '.join(translated_words)

# Read from stdin and print the answer to stdout
import sys
input_sentence = sys.stdin.read().strip()
print(translate_to_nimionese(input_sentence))