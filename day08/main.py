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
            (self.x - other.x)**2
            + (self.y - other.y)**2
            + (self.z - other.z)**2
        )

    def __hash__(self):
        return hash((self.x, self.y, self.z))

    def __repr__(self) -> str:
        return f"({self.x},{self.y},{self.z})"


InputData = list[Pos3D]


def read_input(path: str) -> InputData:
    return [
        Pos3D.from_str(line)
        for line in Path(path).read_text().strip().split("\n")
    ]


def solve_part_one(
    data: InputData,
    target_merged: int,
    top_k: int,
) -> int:
    merge_candidates = sorted(
        [
            ((data[i], data[j]), data[i].distance_to(data[j]))
            for i in range(len(data))
            for j in range(i, len(data))
            if i != j
        ],
        key=lambda v: v[1],
    )

    jbox2circuit = {}
    circuits = {}
    circuit_id = 0
    
    for (p1, p2), dist in merge_candidates[:target_merged]:
        #print(f"Trying {p1}, {p2}...")

        c1 = jbox2circuit.get(p1)
        c2 = jbox2circuit.get(p2)

        if c1 == c2 and c1 is not None:  # Both are in the same circuit
            #print("Same circuit")
            continue
        elif c1 is None and c2 is None:  # Both are not in any circuit
            #print("Both: no circuit")
            circuit_id += 1

            circuits[circuit_id] = {p1, p2}
            jbox2circuit[p1] = circuit_id
            jbox2circuit[p2] = circuit_id
        elif c1 is None and c2 is not None:   # P2 is in a circuit
            #print("P2 in circuit")
            circuits[c2].add(p1)
            jbox2circuit[p1] = c2
        elif c1 is not None and c2 is None:   # P1 is in a circuit
            #print("P1 in circuit")
            circuits[c1].add(p2)
            jbox2circuit[p2] = c1
        else:  # Both are in a circuit (need to merge)
            #print("Both in circuit")
            assert c1 is not None and c2 is not None

            all_nodes = circuits[c1] | circuits[c2]

            circuits.pop(c1)
            circuits.pop(c2)

            circuit_id += 1
            circuits[circuit_id] = all_nodes

            for node in all_nodes:
                jbox2circuit[node] = circuit_id

        #print("Iter end:")
        #print(f"{circuits=}")
        #print(f"{jbox2circuit=}")
        #print("-" * 30)

    circuit_sizes = sorted([len(v) for v in circuits.values()], key=lambda v: -v)

    ans = 1

    for i in range(top_k):
        ans *= circuit_sizes[i]

    return ans


def solve_part_two(data: InputData) -> int:
    ans = 0
    return ans


def test() -> None:
    example_input = read_input("./data/example.txt")
    assert solve_part_one(example_input, target_merged=10, top_k=3) == 40
    assert solve_part_two(example_input) == 0


def main() -> None:
    test()

    _input = read_input("./data/input.txt")

    ans_1 = solve_part_one(_input, target_merged=1000, top_k=3)
    print(f"Part 1: {ans_1}")

    ans_2 = solve_part_two(_input)
    print(f"Part 2: {ans_2}")


if __name__ == "__main__":
    main()
