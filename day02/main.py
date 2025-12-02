"""Day 02"""

from pathlib import Path


InputData = list[tuple[int, int]]


def read_input(path: str) -> InputData:
    out = []

    for r in Path(path).read_text().strip().split(","):
        first_id, last_id = r.split("-")
        out.append((int(first_id), int(last_id)))

    return out


def find_invalid_ids(first_id: int, last_id: int) -> list[int]:
    invalid_ids = []

    for _id in range(first_id, last_id + 1):
        _id = str(_id)

        mid_idx = len(_id) // 2
        left, right = _id[:mid_idx], _id[mid_idx:]

        if left == right:
            invalid_ids.append(int(_id))

    return invalid_ids


def solve_part_one(data: InputData) -> int:
    ans = 0

    for first_id, last_id in data:
        ans += sum(find_invalid_ids(first_id, last_id))

    return ans


def find_invalid_ids_deeper(first_id: int, last_id: int) -> list[int]:
    invalid_ids = []

    for _id in range(first_id, last_id + 1):
        _id = str(_id)

        for pattern_len in range(1, len(_id) // 2 + 1):
            pattern = _id[:pattern_len]

            if all(
                _id[idx : idx + pattern_len] == pattern
                for idx in range(pattern_len, len(_id), pattern_len)
            ):
                invalid_ids.append(int(_id))
                break

    return invalid_ids


def solve_part_two(data: InputData) -> int:
    ans = 0

    for first_id, last_id in data:
        ans += sum(find_invalid_ids_deeper(first_id, last_id))

    return ans


def test() -> None:
    example_input = read_input("./data/example.txt")
    assert solve_part_one(example_input) == 1_227_775_554
    assert solve_part_two(example_input) == 4_174_379_265


def main() -> None:
    test()

    _input = read_input("./data/input.txt")

    ans_1 = solve_part_one(_input)
    print(f"Part 1: {ans_1}")

    ans_2 = solve_part_two(_input)
    print(f"Part 2: {ans_2}")


if __name__ == "__main__":
    main()
