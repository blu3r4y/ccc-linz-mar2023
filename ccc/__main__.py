from pprint import pprint
from pathlib import Path
from funcy import lmap

from loguru import logger as log

from .contest import solve

from collections import namedtuple

RPS = namedtuple("RPS", ["r", "p", "s"])


def load(data):
    first_line = lmap(int, data[0].split(" "))
    n = int(first_line[0])
    m = int(first_line[1])

    expected = []
    for line in data[1:]:
        r, p, s = [int(e[:-1]) for e in line.split(" ")]
        expected.append(RPS(r, p, s))

    return {
        "num_tournaments": n,
        "num_fighters": m,
        "expected": expected,
    }


if __name__ == "__main__":
    level, quests = 4, 0
    for quest in range(quests):
        base_path = Path("data")
        input_file = base_path / f"level{level}_{quest}.in"
        output_file = input_file.with_suffix(".out")

        if not input_file.exists():
            log.warning(f"file not found, skip: {input_file}")
            continue

        with open(input_file, "r") as fi:
            data = load(fi.read().splitlines())
            pprint(data)

            print("=== Input {}".format(quest))
            print("======================")

            right_counts = solve(data)
            pprint(right_counts)

            with open(output_file, "w+") as fo:
                fo.write(right_counts)
