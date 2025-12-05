"""Day 05"""

from pathlib import Path


ProductID = int
ProductIDRange = tuple[ProductID, ProductID]
InputData = tuple[list[ProductIDRange], list[ProductID]]


def read_input(path: str) -> InputData:
    ranges_raw, ids_raw = Path(path).read_text().strip().split("\n\n")

    ranges = []
    for rr in ranges_raw.split("\n"):
        l, r = rr.split("-")
        ranges.append((int(l), int(r)))

    ids = [int(_id) for _id in ids_raw.split("\n")]

    return ranges, ids


def solve_part_one(data: InputData) -> int:
    ans = 0

    ranges, ids = data

    for _id in ids:
        if any(l <= _id <= r for l, r in ranges):
            ans += 1
            continue

    return ans


def can_be_merged(r1: ProductIDRange, r2: ProductIDRange) -> bool:
    return (
        (r1[0] == r2[0])  # Both start at the same ID
        or (r1[1] == r2[1])  # Both end at the same ID
        or (r1[1] >= r2[0])  # They overlap
    )


def solve_part_two(data: InputData) -> int:
    ranges, _ = data

    # Merge ranges
    # Remove any duplicates
    ranges = sorted(set(ranges))

    while True:
        merge_idx = None

        for idx in range(len(ranges) - 1):
            r1, r2 = ranges[idx], ranges[idx + 1]
            if can_be_merged(r1, r2):
                merge_idx = idx
                break

        if merge_idx is None:
            break

        # Merge two ranges
        r1, r2 = ranges[merge_idx], ranges[merge_idx + 1]
        new_r = (min(r1[0], r2[0]), max(r1[1], r2[1]))

        # Update ranges list
        ranges = [*ranges[:merge_idx], new_r, *ranges[merge_idx + 2 :]]

    # Count number of elements in ranges
    ans = 0
    for l, r in ranges:
        ans += r - l + 1

    return ans


def test() -> None:
    example_input = read_input("./data/example.txt")
    assert solve_part_one(example_input) == 3
    assert solve_part_two(example_input) == 14


def main() -> None:
    test()

    _input = read_input("./data/input.txt")

    ans_1 = solve_part_one(_input)
    print(f"Part 1: {ans_1}")

    ans_2 = solve_part_two(_input)
    print(f"Part 2: {ans_2}")


if __name__ == "__main__":
    main()
