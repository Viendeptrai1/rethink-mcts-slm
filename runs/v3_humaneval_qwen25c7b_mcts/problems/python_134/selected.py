def check_if_last_char_is_a_letter(txt):
    if not txt or txt.endswith(' '):
        return False
    for i in range(len(txt) - 1, -1, -1):
        if txt[i] != ' ':
            return txt[i].isalpha() and (i == 0 or txt[i - 1] == ' ')
    return False