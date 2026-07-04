def calculate_pitch(semitones, octave, cents):
    pitch = 440 * (2 ** (octave + ((semitones + (cents / 100)) / 12)))
    return pitch


# print(calculate_pitch(2, -1, 0))
# a = []
# for i in range(0, 12):
#    a.append(calculate_pitch(i, 0, 0))
# print(a)


def lirp(a, b, t):

    dis = b - a
    c = dis * t
    d = a + c
    return d


a = [12, 12, 20]
b = [10, 219, 76]
b2 = [219, 52, 10]
b3 = [104, 13, 1]
c = []
for i in range(40):
    r = lirp(a[0], b[0], i / 40)
    g = lirp(a[1], b[1], i / 40)
    b1 = lirp(a[2], b[2], i / 40)
    c.append((r, g, b1))
for i in range(20):
    r = lirp(b[0], b2[0], i / 20)
    g = lirp(b[1], b2[1], i / 20)
    b1 = lirp(b[2], b2[2], i / 20)
    c.append((r, g, b1))
for i in range(20):
    r = lirp(b2[0], b3[0], i / 20)
    g = lirp(b2[1], b3[1], i / 20)
    b1 = lirp(b2[2], b3[2], i / 20)
    c.append((r, g, b1))
print(c)
