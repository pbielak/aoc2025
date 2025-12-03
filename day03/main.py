"""Day 03"""

from pathlib import Path


InputData = list[str]


def read_input(path: str) -> InputData:
    return Path(path).read_text().strip().split("\n")


def solve_part_one(data: InputData) -> int:
    ans = 0

    for battery_bank in data:
        max_joltage = 0

        for i in range(len(battery_bank) - 1):
            for j in range(i + 1, len(battery_bank)):
                cj = int(f"{battery_bank[i]}{battery_bank[j]}")
                max_joltage = max(max_joltage, cj)

        ans += max_joltage

    return ans


def to_joltage(bank: str, indices: list[int]) -> int:
    return int("".join(bank[i] for i in indices))


def argmax(vals: list) -> int:
    return max(list(enumerate(vals)), key=lambda v: v[1])[0]


def solve_part_two(data: InputData, n_digits: int = 12) -> int:
    ans = 0

    for battery_bank in data:
        indices = []
        left = 0

        for i in reversed(range(n_digits)):
            # Find largest digit within available space
            # Range:
            # - left (next position after last found index)
            # - right (end of battery bank with `i` spaces reserved
            #          for other digits)
            bank = battery_bank[left : len(battery_bank) - i]

            # Use index of this digit
            indices.append(argmax(bank) + left)

            # Adjust search range from the left
            left = indices[-1] + 1

        joltage = to_joltage(battery_bank, indices)
        ans += joltage

    return ans


def test() -> None:
    example_input = read_input("./data/example.txt")
    assert solve_part_one(example_input) == 357
    assert solve_part_two(example_input) == 3_121_910_778_619
    assert solve_part_two(example_input, 2) == solve_part_one(example_input)


def main() -> None:
    test()

    _input = read_input("./data/input.txt")

    ans_1 = solve_part_one(_input)
    print(f"Part 1: {ans_1}")

    ans_2 = solve_part_two(_input)
    print(f"Part 2: {ans_2}")


if __name__ == "__main__":
    main()
