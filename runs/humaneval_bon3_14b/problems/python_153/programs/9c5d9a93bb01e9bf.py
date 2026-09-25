def Strongest_Extension(class_name, extensions):
    def calculate_strength(extension):
        cap = sum(1 for char in extension if char.isupper())
        sm = sum(1 for char in extension if char.islower())
        return cap - sm

    strongest_extension = max(extensions, key=calculate_strength)
    return f"{class_name}.{strongest_extension}"

# Example usage:
# print(Strongest_Extension('Slices', ['SErviNGSliCes', 'Cheese', 'StuFfed']))  # Output: 'Slices.SErviNGSliCes'
# print(Strongest_Extension('my_class', ['AA', 'Be', 'CC']))  # Output: 'my_class.AA'