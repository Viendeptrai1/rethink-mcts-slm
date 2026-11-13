def Strongest_Extension(class_name, extensions):
    strongest = max(extensions, key=lambda ext: sum(1 for c in ext if c.isupper()) - sum(1 for c in ext if c.islower()))
    return f"{class_name}.{strongest}"