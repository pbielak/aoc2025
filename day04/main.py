"""Day 04"""

from pathlib import Path


InputData = list[str]


def read_input(path: str) -> InputData:
    return Path(path).read_text().strip().split("\n")


def find_removable_rolls(data: InputData) -> list[tuple[int, int]]:
    rolls = []

    for row in range(len(data)):
        for col in range(len(data[0])):
            if data[row][col] == ".":
                continue

            adj = [
                data[row + dr][col + dc]
                for dr in (-1, 0, 1)
                for dc in (-1, 0, 1)
                if 0 <= row + dr < len(data)
                and 0 <= col + dc < len(data[0])
                and not (dr == 0 and dc == 0)
            ]

            if adj.count("@") < 4:
                rolls.append((row, col))

    return rolls


def solve_part_one(data: InputData) -> int:
    return len(find_removable_rolls(data))


def solve_part_two(data: InputData) -> int:
    ans = 0

    current_data = [list(line) for line in data]

    while True:
        rr = find_removable_rolls(current_data)

        if len(rr) == 0:
            break

        ans += len(rr)

        for row, col in rr:
            current_data[row][col] = "."

    return ans


def test() -> None:
    example_input = read_input("./data/example.txt")
    assert solve_part_one(example_input) == 13
    assert solve_part_two(example_input) == 43


def main() -> None:
    test()

    _input = read_input("./data/input.txt")

    ans_1 = solve_part_one(_input)
    print(f"Part 1: {ans_1}")

    ans_2 = solve_part_two(_input)
    print(f"Part 2: {ans_2}")


if __name__ == "__main__":
    main()
