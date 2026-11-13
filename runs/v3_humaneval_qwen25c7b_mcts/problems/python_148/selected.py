def bf(planet1, planet2):
    planets = ["Mercury", "Venus", "Earth", "Mars", "Jupiter", "Saturn", "Uranus", "Neptune"]
    try:
        idx1, idx2 = planets.index(planet1), planets.index(planet2)
    except ValueError:
        return ()
    
    start, end = sorted([idx1, idx2])
    return tuple(planets[start + 1:end])

# Example usage:
print(bf("Jupiter", "Neptune"))  # Output: ('Saturn', 'Uranus')
print(bf("Earth", "Mercury"))    # Output: ('Venus',)
print(bf("Mercury", "Uranus"))   # Output: ('Venus', 'Earth', 'Mars', 'Jupiter', 'Saturn')