from funcy import collecting


BEATS = {
    "R": "S",
    "S": "P",
    "P": "R",
}


def play_tournament(tournament):
    while len(tournament) > 1:
        tournament = reduce_tournament(tournament)
    return tournament[0]


def play_rounds(tournament, rounds=2):
    num_rounds = 0
    while num_rounds < rounds:
        tournament = reduce_tournament(tournament)
        num_rounds += 1
    return tournament


def get_winner(a, b):
    if a == b:
        return a
    elif BEATS[a] == b:
        return a
    elif BEATS[b] == a:
        return b


@collecting
def reduce_tournament(tournament):
    if len(tournament) == 1:
        yield tournament[0]
        return

    for i in range(0, len(tournament), 2):
        a = tournament[i]
        b = tournament[i + 1]
        winner = get_winner(a, b)
        yield winner
