from funcy import collecting

BEATS = {
    "R": "S",
    "S": "P",
    "P": "R",
}


def solve(data):
    result = []
    for tournament in data["tournament"]:
        num_rounds = 0
        while num_rounds < 2:
            tournament = _reduce_tournament(tournament)
            num_rounds += 1
        result.append("".join(tournament))

    return "\n".join(result)


def _get_winner(a, b):
    if a == b:
        return a
    elif BEATS[a] == b:
        return a
    elif BEATS[b] == a:
        return b


@collecting
def _reduce_tournament(tournament):
    for i in range(0, len(tournament), 2):
        a = tournament[i]
        b = tournament[i + 1]
        winner = _get_winner(a, b)
        yield winner
