import numpy as np


def get_index(v, arr):
    return np.where(arr == v)


def get_degree(ref, hz):
    log = np.log2(hz / ref) * 360
    return log


# a = np.array([440, 466, 493, 523, 554, 587, 622, 659, 698, 739, 783, 830, 880])

# print(get_degree(440, a))


def findClosest(val, arr):

    leng = len(arr)

    i = int(leng / 2)
    ca = arr

    while True:
        print(ca, val, ca[int(len(ca) // 2)], "\n\n\n")
        if len(ca) == 2:
            if val > np.mean(ca):
                return int(get_index(ca[1], arr)[0][0])
            else:
                return int(get_index(ca[0], arr)[0][0])

        if val > ca[int(len(ca) // 2)]:
            ca = ca[int(len(ca) // 2) :]
        elif val < ca[int(len(ca) // 2)]:
            ca = ca[: int(len(ca) // 2)]
        else:
            return int(get_index(ca[1], val)[0][0])


# a = np.array([0, 2, 5, 6, 7, 10, 12, 20, 50, 60])

# print(findClosest(52, a))
