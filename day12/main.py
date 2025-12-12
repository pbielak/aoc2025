"""Day 12"""

from dataclasses import dataclass
from pathlib import Path


@dataclass
class InputData:
    piece_specs: dict[int, list[str]]
    area_specs: list[tuple[int, int, list[int]]]

    @staticmethod
    def from_str(raw: list[str]) -> "InputData":
        piece_specs = {}
        for line in raw[:-1]:
            _id, shape = line.split(":")
            piece_specs[int(_id)] = shape.strip().split("\n")

        area_specs = []
        for line in raw[-1].split("\n"):
            area_shape, area_reqs = line.split(": ")
            w, h = area_shape.split("x")
            area_reqs = [int(r) for r in area_reqs.split(" ")]

            area_specs.append((int(w), int(h), area_reqs))

        return InputData(piece_specs, area_specs)


def read_input(path: str) -> InputData:
    return InputData.from_str(Path(path).read_text().strip().split("\n\n"))


def solve_part_one(data: InputData) -> int:
    ans = 0

    # Piece size
    pw, ph = len(data.piece_specs[0][0]), len(data.piece_specs[0])

    # Check each area
    for w, h, reqs in data.area_specs:
        minimum_space_req = sum(reqs) * ph * pw
        available_spaces = w * h

        if minimum_space_req <= available_spaces:
            ans += 1

    return ans


def main() -> None:
    _input = read_input("./data/input.txt")

    ans_1 = solve_part_one(_input)
    print(f"Part 1: {ans_1}")


if __name__ == "__main__":
    main()
