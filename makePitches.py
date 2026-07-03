def calculate_pitch(semitones, octave, cents):
    pitch = 440 * (2 ** (octave + ((semitones + (cents / 100)) / 12)))
    return pitch


# print(calculate_pitch(2, -1, 0))
a = []
for i in range(0, 12):
    a.append(calculate_pitch(i, 0, 0))
print(a)
