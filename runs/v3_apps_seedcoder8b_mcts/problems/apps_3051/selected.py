def count_missed_fogs(n, fogs):
    # Sort fogs by their appearance day
    fogs.sort(key=lambda x: x[1])

    # List to store all fogs generated
    all_fogs = []

    # Process each originator fog
    for fog in fogs:
        m_i, d_i, l_i, r_i, h_i, delta_d_i, delta_x_i, delta_h_i = fog
        for k in range(m_i):
            x_start = l_i + k * delta_x_i
            x_end = r_i + k * delta_x_i
            y_start = 0
            y_end = h_i + k * delta_h_i
            all_fogs.append((x_start, x_end, y_start, y_end, d_i + k * delta_d_i))

    # Sort all generated fogs by their appearance day
    all_fogs.sort(key=lambda x: x[4])

    # List to store the current nets
    nets = []

    # Count of missed fogs
    missed_fogs = 0

    # Process each fog
    for fog in all_fogs:
        x_start, x_end, y_start, y_end, day = fog
        # Check if the fog is missed by the current nets
        is_missed = True
        for net in nets:
            nx_start, nx_end, ny_start, ny_end = net
            if x_start >= nx_start and x_end <= nx_end and y_start >= ny_start and y_end <= ny_end:
                is_missed = False
                break
        if is_missed:
            missed_fogs += 1
        # Add the fog to the list of nets
        nets.append((x_start, x_end, y_start, y_end))

    return missed_fogs

# Read input
import sys
input = sys.stdin.read
data = input().split()

n = int(data[0])
fogs = []
index = 1
for _ in range(n):
    m_i = int(data[index])
    d_i = int(data[index + 1])
    l_i = int(data[index + 2])
    r_i = int(data[index + 3])
    h_i = int(data[index + 4])
    delta_d_i = int(data[index + 5])
    delta_x_i = int(data[index + 6])
    delta_h_i = int(data[index + 7])
    fogs.append((m_i, d_i, l_i, r_i, h_i, delta_d_i, delta_x_i, delta_h_i))
    index += 8

# Calculate and print the result
result = count_missed_fogs(n, fogs)
print(result)