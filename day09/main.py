"""Day 09"""

from pathlib import Path

Pos2D = tuple[int, int]
InputData = list[Pos2D]


def read_input(path: str) -> InputData:
    out = []
    for line in Path(path).read_text().strip().split("\n"):
        x, y = line.split(",")
        out.append((int(x), int(y)))
    return out


def solve_part_one(data: InputData) -> int:
    max_area = 0

    for i in range(len(data)):
        for j in range(i + 1, len(data)):
            x_i, y_i = data[i]
            x_j, y_j = data[j]

            area = abs(x_i - x_j + 1) * abs(y_i - y_j + 1)

            max_area = max(max_area, area)

    ans = max_area
    return ans


def solve_part_two(data: InputData) -> int:
    # Compute all rectangles
    rectangles = []
    for i in range(len(data)):
        for j in range(i + 1, len(data)):
            x_i, y_i = data[i]
            x_j, y_j = data[j]
            area = (abs(x_i - x_j) + 1) * (abs(y_i - y_j) + 1)

            rectangles.append((data[i], data[j], area))

    rectangles = sorted(rectangles, key=lambda v: -v[2])
    print(len(rectangles))

    # Collect all perimiter points
    points = set()

    n = len(data)
    for i in range(n):
        x_i, y_i = data[i]
        x_j, y_j = data[(i + 1) % n]

        for x in range(min(x_i, x_j), max(x_i, x_j) + 1):
            for y in range(min(y_i, y_j), max(y_i, y_j) + 1):
                points.add((x, y))

    # Check each rectangle if any perimiter point is on the inside
    for (x_i, y_i), (x_j, y_j), area in rectangles:
        min_x = min(x_i, x_j)
        max_x = max(x_i, x_j)

        min_y = min(y_i, y_j)
        max_y = max(y_i, y_j)

        if any((min_x < x < max_x) and (min_y < y < max_y) for x, y in points):
            continue

        return area


def test() -> None:
    example_input = read_input("./data/example.txt")
    assert solve_part_one(example_input) == 50
    assert solve_part_two(example_input) == 24


def main() -> None:
    test()

    _input = read_input("./data/input.txt")

    ans_1 = solve_part_one(_input)
    print(f"Part 1: {ans_1}")

    ans_2 = solve_part_two(_input)
    print(f"Part 2: {ans_2}")


if __name__ == "__main__":
    main()
