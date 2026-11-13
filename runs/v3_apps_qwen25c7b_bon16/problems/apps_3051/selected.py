def count_missed_fogs(n, fogs):
    total_missed = 0

    for i in range(n):
        mi, di, li, ri, hi, deltadi, deltaxi, deltahi = fogs[i]
        for k in range(mi):
            xi = li + k * deltaxi
            yi = 0
            zi = hi + k * deltahi
            if k == 0:
                start_day = di
            else:
                start_day = di + k * deltadi
            end_day = start_day + deltadi * (mi - 1)
            for day in range(start_day, end_day + 1):
                # Logic to determine if the fog is missed
                missed_fog = True
                for j in range(n):
                    if j != i:
                        mj, dj, lj, rj, hj, deltajdi, deltajxi, deltajhi = fogs[j]
                        for l in range(mj):
                            xj = lj + l * deltajxi
                            yj = 0
                            zj = hj + l * deltajhi
                            if xi >= xj and xi <= rj and yi >= yj and yi <= zj:
                                missed_fog = False
                                break
                        if not missed_fog:
                            break
                if missed_fog:
                    total_missed += 1

    return total_missed

# Example usage:
import sys
input = sys.stdin.read
data = input().split()
index = 0

n = int(data[index])
index += 1
fogs = []
for i in range(n):
    mi = int(data[index])
    di = int(data[index + 1])
    li = int(data[index + 2])
    ri = int(data[index + 3])
    hi = int(data[index + 4])
    deltadi = int(data[index + 5])
    deltaxi = int(data[index + 6])
    deltahi = int(data[index + 7])
    index += 8
    fogs.append((mi, di, li, ri, hi, deltadi, deltaxi, deltahi))

result = count_missed_fogs(n, fogs)
print(result)