def Strongest_Extension(class_name, extensions):
    def calculate_strength(extension):
        upper_count = sum(1 for char in extension if char.isupper())
        lower_count = sum(1 for char in extension if char.islower())
        return upper_count - lower_count

    strongest_extension = None
    max_strength = float('-inf')

    for ext in extensions:
        strength = calculate_strength(ext)
        if strength > max_strength:
            max_strength = strength
            strongest_extension = ext

    return f"{class_name}.{strongest_extension}"