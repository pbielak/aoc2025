"""Day 11"""

from dataclasses import dataclass
from pathlib import Path


@dataclass
class Graph:
    nodes: set[str]
    adj: dict[str, list[str]]

    @staticmethod
    def from_edge_list(raw: list[str]) -> "Graph":
        nodes = set()
        adj = {}

        for line in raw:
            node, neighs = line.split(": ")

            nodes.add(node)
            nodes.update(neighs.split(" "))
            adj[node] = neighs.split(" ")

        return Graph(nodes, adj)


def read_input(path: str) -> Graph:
    return Graph.from_edge_list(Path(path).read_text().strip().split("\n"))


def find_all_paths(
    graph: Graph,
    start_node: str,
    end_node: str,
) -> list[list[str]]:
    paths = []

    queue = [(start_node,)]

    while queue:
        path = queue.pop(0)

        for n in graph.adj.get(path[-1], []):
            new_path = [*path, n]

            if n == end_node:
                paths.append(new_path)
                continue

            queue.append(new_path)

    return paths


def solve_part_one(g: Graph) -> int:
    paths = find_all_paths(graph=g, start_node="you", end_node="out")
    ans = len(paths)
    return ans


def find_n_paths(
    graph: Graph,
    start_node: str,
    end_node: str,
    cache: dict[str, int],
) -> int:
    if start_node == end_node:
        return 1

    if start_node in cache:
        return cache[start_node]

    cache[start_node] = sum(
        find_n_paths(graph, neigh, end_node, cache)
        for neigh in graph.adj.get(start_node, [])
    )
    return cache[start_node]


def solve_part_two(g: Graph) -> int:
    cache = {}
    svr_fft = find_n_paths(graph=g, start_node="svr", end_node="fft", cache=cache)
    dac_fft = find_n_paths(graph=g, start_node="dac", end_node="fft", cache=cache)

    cache = {}
    svr_dac = find_n_paths(graph=g, start_node="svr", end_node="dac", cache=cache)
    fft_dac = find_n_paths(graph=g, start_node="fft", end_node="dac", cache=cache)

    cache = {}
    dac_out = find_n_paths(graph=g, start_node="dac", end_node="out", cache=cache)
    fft_out = find_n_paths(graph=g, start_node="fft", end_node="out", cache=cache)

    ans = svr_fft * fft_dac * dac_out + svr_dac * dac_fft * fft_out
    return ans


def test() -> None:
    example_input = read_input("./data/example.txt")
    assert solve_part_one(example_input) == 5
    example_input_2 = read_input("./data/example2.txt")
    assert solve_part_two(example_input_2) == 2


def main() -> None:
    test()

    _input = read_input("./data/input.txt")

    ans_1 = solve_part_one(_input)
    print(f"Part 1: {ans_1}")

    ans_2 = solve_part_two(_input)
    print(f"Part 2: {ans_2}")


if __name__ == "__main__":
    main()
