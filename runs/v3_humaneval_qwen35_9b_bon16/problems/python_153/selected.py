def Strongest_Extension(class_name, extensions):
    def calculate_strength(ext):
        cap = sum(1 for c in ext if c.isupper())
        sm = sum(1 for c in ext if c.islower())
        return cap - sm
    
    strongest_ext = None
    max_strength = float('-inf')
    
    for ext in extensions:
        strength = calculate_strength(ext)
        if strength > max_strength:
            max_strength = strength
            strongest_ext = ext
            
    return f"{class_name}.{strongest_ext}"