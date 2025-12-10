"""Day 10"""

from dataclasses import dataclass
from pathlib import Path


@dataclass
class MachineEntry:
    target: list[int]
    buttons: list[tuple[int]]
    joltages: list[int]

    @staticmethod
    def from_str(raw: str) -> "MachineEntry":
        target, *buttons, joltages = raw.split(" ")

        target = [1 if c == "#" else 0 for c in target[1:-1]]
        buttons = [tuple(int(b) for b in bs[1:-1].split(",")) for bs in buttons]
        joltages = [int(j) for j in joltages[1:-1].split(",")]

        return MachineEntry(target, buttons, joltages)


InputData = list[MachineEntry]


def read_input(path: str) -> InputData:
    return [
        MachineEntry.from_str(line)
        for line in Path(path).read_text().strip().split("\n")
    ]


def find_min_clicks_activate(entry: MachineEntry) -> int:
    # BFS - try to click each button
    queue = [
        # current state, button to press, num_clicks
        (
            [
                0,
            ]
            * len(entry.target),
            btn,
            0,
        )
        for btn in entry.buttons
    ]

    visited_states = set()  # (state, button)

    while queue:
        state, button, n_clicks = queue.pop(0)

        # Check if we already have seen the current state
        # If yes - it doesn't make sense to press the button again (loop)
        if (tuple(state), button) in visited_states:
            continue

        visited_states.add((tuple(state), button))

        # Apply button click
        new_state = state.copy()
        for idx in button:
            new_state[idx] = 1 if new_state[idx] == 0 else 0  # Invert state

        # Check if done
        if new_state == entry.target:
            return n_clicks + 1

        queue.extend([(new_state, btn, n_clicks + 1) for btn in entry.buttons])


def solve_part_one(data: InputData) -> int:
    ans = 0

    for entry in data:
        min_clicks = find_min_clicks_activate(entry)
        ans += min_clicks

    return ans


def find_min_clicks_joltage(entry: MachineEntry) -> int:
    from scipy.optimize import linprog

    # Apply linear programming
    coefs = [
        1,
    ] * len(entry.buttons)
    A = [[0 for _ in range(len(entry.buttons))] for _ in range(len(entry.joltages))]

    for b_idx, button in enumerate(entry.buttons):
        for idx in button:
            A[idx][b_idx] = 1

    # We want A_eq @ x = b_eq, where sum(x) is minimal (so coef = [1, ..., 1])
    res = linprog(
        c=coefs,
        A_eq=A,
        b_eq=entry.joltages,
        integrality=1,
    )

    return int(res.fun)


def solve_part_two(data: InputData) -> int:
    ans = 0

    for entry in data:
        min_clicks = find_min_clicks_joltage(entry)
        ans += min_clicks

    return ans


def test() -> None:
    example_input = read_input("./data/example.txt")
    assert solve_part_one(example_input) == 7
    assert solve_part_two(example_input) == 33


def main() -> None:
    test()

    _input = read_input("./data/input.txt")

    ans_1 = solve_part_one(_input)
    print(f"Part 1: {ans_1}")

    ans_2 = solve_part_two(_input)
    print(f"Part 2: {ans_2}")


if __name__ == "__main__":
    main()
