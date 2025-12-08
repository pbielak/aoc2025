"""Day 08"""

import math
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Pos3D:
    x: int
    y: int
    z: int

    @staticmethod
    def from_str(raw: str) -> "Pos3D":
        x, y, z = raw.split(",")
        return Pos3D(int(x), int(y), int(z))

    def distance_to(self, other: "Pos3D") -> int:
        return math.sqrt(
            (self.x - other.x) ** 2 + (self.y - other.y) ** 2 + (self.z - other.z) ** 2
        )

    def __hash__(self):
        return hash((self.x, self.y, self.z))

    def __repr__(self) -> str:
        return f"({self.x},{self.y},{self.z})"


InputData = list[Pos3D]


def read_input(path: str) -> InputData:
    return [Pos3D.from_str(line) for line in Path(path).read_text().strip().split("\n")]


def merge_jboxes(
    data: InputData,
    max_merged: int = -1,
) -> dict[int, set[Pos3D]] | tuple[Pos3D, Pos3D]:
    circuits = {}
    jbox2circuit = {}

    for i, jbox in enumerate(data):
        circuits[i] = {jbox}
        jbox2circuit[jbox] = i

    merge_candidates = sorted(
        [
            ((data[i], data[j]), data[i].distance_to(data[j]))
            for i in range(len(data))
            for j in range(i + 1, len(data))
        ],
        key=lambda v: v[1],
    )

    if max_merged != -1:
        merge_candidates = merge_candidates[:max_merged]

    for (p1, p2), dist in merge_candidates:
        c1 = jbox2circuit[p1]
        c2 = jbox2circuit[p2]

        if c1 == c2:  # Both are in the same circuit
            continue
        else:  # Different circuits
            all_nodes = circuits[c1] | circuits[c2]

            circuits.pop(c1)
            circuits.pop(c2)

            circuits[c1] = all_nodes

            for node in all_nodes:
                jbox2circuit[node] = c1

        if max_merged == -1 and len(circuits) == 1:  # Stop if merged
            return p1, p2

    return circuits


def solve_part_one(
    data: InputData,
    max_merged: int,
    top_k: int,
) -> int:
    circuits = merge_jboxes(data, max_merged=max_merged)

    circuit_sizes = sorted([len(v) for v in circuits.values()], key=lambda v: -v)

    ans = 1

    for i in range(top_k):
        ans *= circuit_sizes[i]

    return ans


def solve_part_two(data: InputData) -> int:
    p1, p2 = merge_jboxes(data, max_merged=-1)
    ans = p1.x * p2.x
    return ans


def test() -> None:
    example_input = read_input("./data/example.txt")
    assert solve_part_one(example_input, max_merged=10, top_k=3) == 40
    assert solve_part_two(example_input) == 25_272


def main() -> None:
    test()

    _input = read_input("./data/input.txt")

    ans_1 = solve_part_one(_input, max_merged=1000, top_k=3)
    print(f"Part 1: {ans_1}")

    ans_2 = solve_part_two(_input)
    print(f"Part 2: {ans_2}")


if __name__ == "__main__":
    main()
