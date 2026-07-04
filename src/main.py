#!/usr/bin/env python3
"""Show a text-mode spectrogram using live microphone data."""

import argparse
import math
import shutil
from random import random

import numpy as np
import pygame
import pygame_widgets
import sounddevice as sd
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox

import randomShi

usage_line = " press <enter> to quit, +<enter> or -<enter> to change scaling "


# trig wrapper to make it work in degrees since im a chud
def trig_wrapper(func):
    def inner(*args, **kwargs):
        args = [
            math.radians(arg) if isinstance(arg, (int, float)) else arg for arg in args
        ]
        return func(*args, **kwargs)

    return inner


for func_name in ["sin", "cos", "tan"]:
    setattr(math, func_name, trig_wrapper(getattr(math, func_name)))


def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text


try:
    columns, _ = shutil.get_terminal_size()
except AttributeError:
    columns = 80

columns = 20000


parser = argparse.ArgumentParser(add_help=False)
parser.add_argument(
    "-l",
    "--list-devices",
    action="store_true",
    help="show list of audio devices and exit",
)
args, remaining = parser.parse_known_args()
if args.list_devices:
    print(sd.query_devices())
    parser.exit(0)
parser = argparse.ArgumentParser(
    description=__doc__ + "\n\nSupported keys:" + usage_line,  # type: ignore
    formatter_class=argparse.RawDescriptionHelpFormatter,
    parents=[parser],
)
parser.add_argument(
    "-b",
    "--block-duration",
    type=float,
    metavar="DURATION",
    default=50,
    help="block size (default %(default)s milliseconds)",
)
parser.add_argument(
    "-c", "--columns", type=int, default=columns, help="width of spectrogram"
)
parser.add_argument(
    "-d", "--device", type=int_or_str, help="input device (numeric ID or substring)"
)
parser.add_argument(
    "-g",
    "--gain",
    type=float,
    default=10,
    help="initial gain factor (default %(default)s)",
)
parser.add_argument(
    "-r",
    "--range",
    type=float,
    nargs=2,
    metavar=("LOW", "HIGH"),
    default=[110, 4183],
    help="frequency range (default %(default)s Hz)",
)
args = parser.parse_args(remaining)
low, high = args.range
if high <= low:
    parser.error("HIGH must be greater than LOW")


# import stuff stars here
samplerate = sd.query_devices(args.device, "input")["default_samplerate"]

# pygame setiup
pygame.init()
screen = pygame.display.set_mode((900, 1000))
screen2 = pygame.display.set_mode((900, 1000))
pygame.display.set_caption("Squricles")
screen.fill((12, 12, 20))
gainS = slider = Slider(
    screen2,
    100,
    950,
    600,
    20,
    min=1,
    max=200,
    step=1,
    colour=(20, 20, 20),
    handleColour=(200, 200, 210),
    valueColour=(60, 60, 60),
    inital=124,
)

pygame.display.flip()


def calc_real_bins():
    # hrz frequcy map
    frequencies = np.fft.rfftfreq(fftsize, d=1 / samplerate)
    # degree map
    f2 = randomShi.get_degree(110, frequencies)

    # culling mask creaton
    mask = np.zeros(len(f2))
    mask = mask.astype(bool)
    last = -1000000
    # loop
    for i in range(len(f2)):
        if (f2[i] >= 0) & (f2[i] <= 360 * 8):
            if (f2[i] - last) >= 0.5:
                last = f2[i]
                mask[i] = True
    # print(mask)
    # print("calc")
    # print(np.extract(mask, f2).astype(int)[100:115])
    return mask
    # cull = (f2 >= 0) & (f2 <= 360 * 8)
    # f3 = np.extract(cull, f2)

    # print(cull, f3[:10], len(f3), len(f2))


colors = [
    (12.0, 12.0, 35.0),
    (11.95, 17.175, 21.4),
    (11.9, 22.35, 22.8),
    (11.85, 27.525, 24.2),
    (11.8, 32.7, 25.6),
    (11.75, 37.875, 27.0),
    (11.7, 43.05, 28.4),
    (11.65, 48.224999999999994, 29.799999999999997),
    (11.6, 53.400000000000006, 31.200000000000003),
    (11.55, 58.575, 32.6),
    (11.5, 63.75, 34.0),
    (11.45, 68.92500000000001, 35.400000000000006),
    (11.4, 74.1, 36.8),
    (11.35, 79.275, 38.2),
    (11.3, 84.44999999999999, 39.599999999999994),
    (11.25, 89.625, 41.0),
    (11.2, 94.80000000000001, 42.400000000000006),
    (11.15, 99.975, 43.8),
    (11.1, 105.15, 45.2),
    (11.05, 110.32499999999999, 46.599999999999994),
    (11.0, 115.5, 48.0),
    (10.95, 120.67500000000001, 49.400000000000006),
    (10.9, 125.85000000000001, 50.800000000000004),
    (10.85, 131.02499999999998, 52.199999999999996),
    (10.8, 136.2, 53.6),
    (10.75, 141.375, 55.0),
    (10.7, 146.55, 56.4),
    (10.65, 151.72500000000002, 57.800000000000004),
    (10.6, 156.89999999999998, 59.199999999999996),
    (10.55, 162.075, 60.6),
    (10.5, 167.25, 62.0),
    (10.45, 172.425, 63.4),
    (10.4, 177.60000000000002, 64.80000000000001),
    (10.35, 182.77499999999998, 66.19999999999999),
    (10.3, 187.95, 67.6),
    (10.25, 193.125, 69.0),
    (10.2, 198.3, 70.4),
    (10.15, 203.47500000000002, 71.80000000000001),
    (10.1, 208.64999999999998, 73.19999999999999),
    (10.05, 213.825, 74.6),
    (10.0, 219.0, 76.0),
    (20.450000000000003, 210.65, 72.7),
    (30.900000000000002, 202.3, 69.4),
    (41.349999999999994, 193.95, 66.1),
    (51.800000000000004, 185.6, 62.8),
    (62.25, 177.25, 59.5),
    (72.69999999999999, 168.9, 56.2),
    (83.14999999999999, 160.55, 52.900000000000006),
    (93.60000000000001, 152.2, 49.599999999999994),
    (104.05, 143.85, 46.3),
    (114.5, 135.5, 43.0),
    (124.95, 127.14999999999999, 39.699999999999996),
    (135.39999999999998, 118.8, 36.4),
    (145.85, 110.45, 33.1),
    (156.29999999999998, 102.10000000000001, 29.800000000000004),
    (166.75, 93.75, 26.5),
    (177.20000000000002, 85.4, 23.199999999999996),
    (187.65, 77.05000000000001, 19.9),
    (198.1, 68.69999999999999, 16.6),
    (208.54999999999998, 60.349999999999994, 13.300000000000004),
    (219.0, 52.0, 10.0),
    (213.25, 50.05, 9.55),
    (207.5, 48.1, 9.1),
    (201.75, 46.15, 8.65),
    (196.0, 44.2, 8.2),
    (190.25, 42.25, 7.75),
    (184.5, 40.3, 7.300000000000001),
    (178.75, 38.35, 6.85),
    (173.0, 36.4, 6.4),
    (167.25, 34.45, 5.95),
    (161.5, 32.5, 5.5),
    (155.75, 30.549999999999997, 5.05),
    (150.0, 28.6, 4.6000000000000005),
    (144.25, 26.65, 4.1499999999999995),
    (138.5, 24.700000000000003, 3.7),
    (132.75, 22.75, 3.25),
    (127.0, 20.799999999999997, 2.8),
    (121.25, 18.85, 2.3500000000000005),
    (115.5, 16.9, 1.9000000000000004),
    (109.75, 14.950000000000003, 1.450000000000001),
]


def make_bins():
    frequencies = np.fft.rfftfreq(fftsize, d=1 / samplerate)
    # degree map
    f2 = randomShi.get_degree(110, frequencies)
    return np.extract(fMask, f2)


font = pygame.font.SysFont("timesnewroman", 30)


def draw_guides():
    textRef = ["A", "Bb", "B", "C", "C#", "D", "Eb", "E", "F", "F#", "G", "Ab"]
    mukt3 = 30
    for i in range(0, 350, int(360 / 12)):
        mult = 400 - ((i / 360) * 40) + 20
        x1 = (math.sin(i) * mult) + 450
        y1 = (-math.cos(i) * mult) + 450
        x2 = (math.sin(i) * mukt3) + 450
        y2 = (-math.cos(i) * mukt3) + 450
        x3 = (math.sin(i) * (mult + 20)) + 450
        y3 = (-math.cos(i) * (mult + 20)) + 450
        pygame.draw.line(screen, (99, 99, 99), (x1, y1), (x2, y2), 2)
        text = font.render(textRef[int(i / 30)], True, (255, 255, 255), (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (x3, y3)
        screen.blit(text, textRect)


def draw_line(s, t, max, change, color, width):
    mult = max - ((t / 360) * change)
    mult2 = (max - change) - ((t / 360) * change)

    x1 = (math.sin(t) * mult) + 450
    y1 = (-math.cos(t) * mult) + 450

    x2 = (math.sin(t) * mult2) + 450
    y2 = (math.cos(t) * -mult2) + 450

    pygame.draw.line(s, color, (x1, y1), (x2, y2), int(width))


fMask = []
bins = []
gain = 0.008
try:

    def callback(indata, frames, time, status):
        # ts gonna larp as the main loop lol

        # i was wrong. it aint

        global fMask
        global bins
        global screen
        global gain
        if status:
            print(status)
        if any(indata):
            magnitude = np.abs(np.fft.rfft(indata[:, 0], n=fftsize))

            # this is all the buckets
            magnitudes = np.abs(magnitude)

            # get the mask on the first time
            if type(fMask).__name__ == "list":
                fMask = calc_real_bins()
                bins = make_bins()
            sets = np.extract(fMask, magnitudes)
            sets = np.power(sets, 2) * (gain)

            for i in range(len(bins)):
                draw_line(screen, bins[i], 400, 40, colors[min(int(sets[i]), 79)], 7)
            draw_guides()
            pygame.display.flip()
            # print(bins)

            # create magintude via mask

            # print(sets)

            # this is the locations of all the buckets

            # maxofM = magnitude.index(max(magnitudes))
            # maxofM = np.where(magnitude == max(magnitudes))
            # maxofM1 = randomShi.get_index(max(magnitudes), magnitude)
            # maxofM = frequencies[int(maxofM1[0][0])]

            # a = randomShi.findClosest(maxofM, bins)

            # print(names[int(np.where(bins == a)[0][0])])

            # print(set, names[int(set.index(max(set)) / 5)])

            # aMask = (frequencies >= 435) & (frequencies <= 445)
            # print(np.mean(magnitudes[aMask]))

    delta_f = (high - low) / (args.columns - 1)
    fftsize = math.ceil(samplerate / delta_f)
    low_bin = math.floor(low / delta_f)

    with sd.InputStream(
        device=args.device,
        channels=1,
        callback=callback,
        blocksize=int(samplerate * args.block_duration / 1000),
        samplerate=samplerate,
    ):
        while True:
            # ts is actually the main loop
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    parser.exit(1, "\nInterrupted by user")
                gain = 1 / (int(slider.getValue()))
                pygame.draw.rect(screen2, (12, 12, 20), pygame.Rect(0, 900, 900, 100))
                pygame_widgets.update(events)
                pygame.display.update()


except KeyboardInterrupt:
    print("-------------------------")
    # for i in last:
    #     print(i)
    parser.exit(1, "\nInterrupted by user")
