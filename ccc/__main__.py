from pprint import pprint
from pathlib import Path
from funcy import lmap

from loguru import logger as log

from .contest import solve


def load(data):
    first_line = lmap(int, data[0].split(" "))
    n = int(first_line[0])
    m = int(first_line[1])

    styles = []
    for style in data[1:]:
        styles.append(tuple(style))

    assert n == len(styles)

    return {
        "num_tournaments": n,
        "num_fighters": m,
        "tournament": styles,
    }


if __name__ == "__main__":
    level, quests = 2, 6
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

            result = solve(data)
            pprint(result)

            with open(output_file, "w+") as fo:
                fo.write(result)
