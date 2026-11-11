def file_name_check(file_name):
    def has_valid_extension(name):
        valid_extensions = {'txt', 'exe', 'dll'}
        parts = name.split('.')
        return len(parts) == 2 and parts[1] in valid_extensions

    def starts_with_letter(name):
        return name and name[0].isalpha()

    def has_valid_digit_count(name):
        return sum(c.isdigit() for c in name) <= 3

    def contains_single_dot(name):
        return name.count('.') == 1

    if (contains_single_dot(file_name) and
        starts_with_letter(file_name.split('.')[0]) and
        has_valid_digit_count(file_name) and
        has_valid_extension(file_name)):
        return 'Yes'
    else:
        return 'No'