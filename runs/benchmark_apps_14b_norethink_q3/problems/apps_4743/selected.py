import sys

def translate_to_nimionese(sentence):
    def nearest_hard_consonant(c):
        hard_consonants = 'bcdfghjklmnpqrstvwxyz'
        index = hard_consonants.index(c.lower())
        return hard_consonants[index]

    def replace_hard_consonants(word, first_consonant):
        result = []
        for char in word:
            if char.lower() in 'bcdfghjklmnpqrstvwxyz':
                result.append(first_consonant)
            else:
                result.append(char)
        return ''.join(result)

    def add_ending(word):
        last_consonant = None
        for char in reversed(word):
            if char.lower() in 'bcdfghjklmnpqrstvwxyz':
                last_consonant = char
                break
        if last_consonant is None:
            return word + 'ah'
        if last_consonant.lower() <= 'g':
            return word + 'ah'
        elif last_consonant.lower() <= 'n':
            return word + 'oh'
        else:
            return word + 'uh'

    words = sentence.split()
    translated_words = []

    for word in words:
        word = word.replace('-', '')
        if word.lower() == 'each':
            translated_word = 'Dach'
        else:
            first_consonant = nearest_hard_consonant(word[0])
            translated_word = replace_hard_consonants(word, first_consonant)
            translated_word = add_ending(translated_word)
        translated_words.append(translated_word)

    return ' '.join(translated_words)

if __name__ == "__main__":
    input_sentence = sys.stdin.read().strip()
    output_sentence = translate_to_nimionese(input_sentence)
    print(output_sentence)