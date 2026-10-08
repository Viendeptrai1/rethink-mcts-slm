import sys

def translate_to_nimionese(sentence):
    hard_consonants = 'bcdfgknpt'
    replacements = {
        'a': 'b', 'b': 'b', 'c': 'c', 'd': 'd', 'e': 'd', 'f': 'f', 'g': 'g',
        'h': 'g', 'i': 'k', 'j': 'k', 'k': 'k', 'l': 'n', 'm': 'n', 'n': 'n',
        'o': 'p', 'p': 'p', 'q': 't', 'r': 't', 's': 't', 't': 't', 'u': 'b',
        'v': 'b', 'w': 'b', 'x': 'b', 'y': 'b', 'z': 'b'
    }
    
    def replace_first_letter(word):
        if word.lower() == 'each':
            return 'Dach'
        first_letter = word[0].lower()
        new_first_letter = replacements[first_letter]
        return new_first_letter + word[1:]
    
    def replace_hard_consonants(word):
        new_word = ''
        for i, char in enumerate(word):
            if char.lower() in hard_consonants and i > 0:
                new_word += new_word[0]
            else:
                new_word += char
        return new_word
    
    def add_ending(word):
        if word[-1].lower() in hard_consonants:
            word += 'ah'
        else:
            last_hard_consonant_index = -1
            for i in range(len(word) - 1, -1, -1):
                if word[i].lower() in hard_consonants:
                    last_hard_consonant_index = i
                    break
            if last_hard_consonant_index != -1:
                word += 'ah' if word[last_hard_consonant_index].lower() <= 'm' else 'oh'
            else:
                word += 'ah'
        return word
    
    words = sentence.split()
    translated_words = []
    
    for word in words:
        word = word.replace('-', '')
        word = replace_first_letter(word)
        word = replace_hard_consonants(word)
        word = add_ending(word)
        translated_words.append(word)
    
    return ' '.join(translated_words)

if __name__ == "__main__":
    input_sentence = sys.stdin.read().strip()
    output_sentence = translate_to_nimionese(input_sentence)
    print(output_sentence)