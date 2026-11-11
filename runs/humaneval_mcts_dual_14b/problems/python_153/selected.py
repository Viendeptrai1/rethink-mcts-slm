def Strongest_Extension(class_name, extensions):
    def calculate_strength(extension):
        cap = sum(1 for c in extension if c.isupper())
        sm = sum(1 for c in extension if c.islower())
        return cap - sm

    strongest_extension = max(extensions, key=calculate_strength)
    return f"{class_name}.{strongest_extension}"