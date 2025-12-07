"""Day 07"""

from pathlib import Path


InputData = list[str]


def read_input(path: str) -> InputData:
    return Path(path).read_text().strip().split("\n")


def solve_part_one(data: InputData) -> int:
    ans = 0

    start_pos = data[0].index("S")

    beams = {start_pos}

    for line in data[1:]:
        for idx, c in enumerate(line):
            if c == "^" and idx in beams:
                beams.remove(idx)
                beams.add(idx - 1)
                beams.add(idx + 1)
                ans += 1

    return ans


def solve_part_two(data: InputData) -> int:
    beams = [
        0,
    ] * len(data[0])

    start_pos = data[0].index("S")
    beams[start_pos] += 1

    for line in data[1:]:
        for idx, c in enumerate(line):
            if c == "^" and beams[idx] > 0:
                beams[idx - 1] += beams[idx]
                beams[idx + 1] += beams[idx]
                beams[idx] = 0

    ans = sum(beams)

    return ans


def test() -> None:
    example_input = read_input("./data/example.txt")
    assert solve_part_one(example_input) == 21
    assert solve_part_two(example_input) == 40


def main() -> None:
    test()

    _input = read_input("./data/input.txt")

    ans_1 = solve_part_one(_input)
    print(f"Part 1: {ans_1}")

    ans_2 = solve_part_two(_input)
    print(f"Part 2: {ans_2}")


if __name__ == "__main__":
    main()
