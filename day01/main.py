"""Day 01"""

from pathlib import Path


def rotate_dial(
    instructions: list[str],
    start_pos: int = 50,
    advanced_method: bool = False,
) -> int:
    """Returns the number of times the dial is at position 0."""

    pos = start_pos
    zero_cnt = 0

    for ins in instructions:
        direction, offset = ins[0], int(ins[1:])
        if direction == "L":
            offset *= -1

        if advanced_method:
            rot, offset = abs(offset) // 100, abs(offset) % 100

            if direction == "L":
                offset *= -1

            zero_cnt += rot

            if pos != 0:
                if pos + offset > 100 or pos + offset < 0:
                    zero_cnt += 1

        pos = (pos + offset) % 100

        if pos == 0:
            zero_cnt += 1

    return zero_cnt


def test():
    example_in = ["L68", "L30", "R48", "L5", "R60", "L55", "L1", "L99", "R14", "L82"]
    assert rotate_dial(example_in) == 3
    assert rotate_dial(example_in, advanced_method=True) == 6


def main() -> None:
    test()

    input_data = Path("./data/input.txt").read_text().strip().split("\n")
    ans_1 = rotate_dial(input_data)
    print(f"Part 1: {ans_1}")

    ans_2 = rotate_dial(input_data, advanced_method=True)
    print(f"Part 2: {ans_2}")


if __name__ == "__main__":
    main()
