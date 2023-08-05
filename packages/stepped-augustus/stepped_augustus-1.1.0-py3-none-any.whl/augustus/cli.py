import argparse
import sys

from augustus.cipher import SteppedAugustus


def non_zero_integer(value):
    if int(value) == 0:
        msg = "must be non-zero"
        raise argparse.ArgumentTypeError(msg)
    return int(value)


def main():
    parser = argparse.ArgumentParser(description="Ciphers a given message.")
    parser.add_argument("message", help="The message to be ciphered", type=str)
    parser.add_argument(
        "--direction",
        choices=("left", "right"),
        default="right",
        help="The direction to cipher the message to",
        type=str,
    )
    parser.add_argument(
        "--multiplier",
        help="The multiplier to be applied when ciphering a message",
        default=1,
        type=non_zero_integer,
    )

    args = parser.parse_args()

    if args.message == None:
        parser.print_help(sys.stderr)
        sys.exit(1)

    message = SteppedAugustus(args.message, args.multiplier)

    if args.direction == "right":
        print(message.right_cipher)

    else:
        print(message.left_cipher)
