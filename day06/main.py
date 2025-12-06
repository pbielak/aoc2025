"""Day 06"""

import re
from functools import reduce
from operator import add, mul
from pathlib import Path


InputData = list[str]

OPS = {"+": add, "*": mul}


def read_input(path: str) -> InputData:
    return [line for line in Path(path).read_text().split("\n") if line]


def solve_part_one(data: InputData) -> int:
    ans = 0

    problems = [re.findall(r"\d+|[\*\+]", line) for line in data]
    num_problems = len(problems[0])
    assert all(len(problem) == num_problems for problem in problems[1:])

    for idx in range(num_problems):
        op = OPS[problems[-1][idx]]
        numbers = [int(line[idx]) for line in problems[:-1]]

        ans += reduce(op, numbers)

    return ans


def solve_part_two(data: InputData) -> int:
    ans = 0

    n_cols = len(data[0])
    assert all(len(line) == n_cols for line in data)

    numbers = []
    for col_idx in reversed(range(n_cols)):
        col = "".join(line[col_idx] for line in data)

        if col.strip() == "":
            continue
        elif col[-1] in ("+", "*"):
            op = OPS[col[-1]]

            numbers.append(int(col[:-1]))

            ans += reduce(op, numbers)
            numbers = []
        else:
            numbers.append(int(col))

    return ans


def test() -> None:
    example_input = read_input("./data/example.txt")
    assert solve_part_one(example_input) == 4_277_556
    assert solve_part_two(example_input) == 3_263_827


def main() -> None:
    test()

    _input = read_input("./data/input.txt")

    ans_1 = solve_part_one(_input)
    print(f"Part 1: {ans_1}")

    ans_2 = solve_part_two(_input)
    print(f"Part 2: {ans_2}")


if __name__ == "__main__":
    main()
