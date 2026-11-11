def bf(planet1, planet2):
    planets = ["Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune"]
    
    if planet1 not in planets or planet2 not in planets:
        return ()
    
    index1 = planets.index(planet1)
    index2 = planets.index(planet2)
    
    if index1 < index2:
        return tuple(planets[index1 + 1:index2])
    else:
        return tuple(planets[index2 + 1:index1])

# Example usage:
# print(bf("Jupiter", "Neptune"))  # Output: ("Saturn", "Uranus")
# print(bf("Earth", "Mercury"))    # Output: ("Venus",)
# print(bf("Mercury", "Uranus"))   # Output: ("Venus", "Earth", "Mars", "Jupiter", "Saturn")