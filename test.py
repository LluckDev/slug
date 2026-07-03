#!/usr/bin/env python3
"""Show a text-mode spectrogram using live microphone data."""

import argparse
import math
import shutil

import numpy as np
import sounddevice as sd

import randomShi

usage_line = " press <enter> to quit, +<enter> or -<enter> to change scaling "


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
    default=[100, 2000],
    help="frequency range (default %(default)s Hz)",
)
args = parser.parse_args(remaining)
low, high = args.range
if high <= low:
    parser.error("HIGH must be greater than LOW")


colors = 30, 34, 35, 91, 93, 97
chars = " :%#\t#%:"
gradient = []
for bg, fg in zip(colors, colors[1:]):
    for char in chars:
        if char == "\t":
            bg, fg = fg, bg
        else:
            gradient.append(f"\x1b[{fg};{bg + 10}m{char}")


samplerate = sd.query_devices(args.device, "input")["default_samplerate"]

last = np.zeros(1811)

bins = np.array(
    [
        440.0,
        466.1637615180899,
        493.8833012561241,
        523.2511306011972,
        554.3652619537442,
        587.3295358348151,
        622.2539674441618,
        659.2551138257398,
        698.4564628660078,
        739.9888454232688,
        783.9908719634985,
        830.6093951598903,
    ]
)

names = [
    "A",
    "Bb",
    "B",
    "C",
    "C#",
    "D",
    "Db",
    "E",
    "Eb",
    "E",
    "F",
    "F#",
    "G",
    "G#",
]


try:

    def callback(indata, frames, time, status):
        if status:
            print(status)
        if any(indata):
            magnitude = np.abs(np.fft.rfft(indata[:, 0], n=fftsize))
            magnitudes = np.abs(magnitude)
            frequencies = np.fft.rfftfreq(fftsize, d=1 / samplerate)

            # maxofM = magnitude.index(max(magnitudes))
            # maxofM = np.where(magnitude == max(magnitudes))
            maxofM1 = randomShi.get_index(max(magnitudes), magnitude)
            maxofM = frequencies[int(maxofM1[0][0])]

            a = randomShi.findClosest(maxofM, bins)

            print(names[int(np.where(bins == a)[0][0])])

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
            response = input()
            if response in ("", "q", "Q"):
                break
            for ch in response:
                if ch == "+":
                    args.gain *= 2
                elif ch == "-":
                    args.gain /= 2
                else:
                    print(
                        "\x1b[31;40m",
                        usage_line.center(args.columns, "#"),
                        "\x1b[0m",
                        sep="",
                    )
                    break
except KeyboardInterrupt:
    print("-------------------------")
    # for i in last:
    #     print(i)
    parser.exit(1, "\nInterrupted by user")
