from funcy import collecting

BEATS = {
    "R": "S",
    "S": "P",
    "P": "R",
}


def solve(data):
    result = []
    for exp in data["expected"]:
        tournament = _determine_pairing(exp.r, exp.p, exp.s)
        result.append("".join(tournament))
        assert _verify_pairing(tournament)

    return "\n".join(result)


def _determine_pairing(r, p, s):
    pairing = []

    # pair as much Rs as possible
    while r >= 3:
        assert p > 0
        pairing.extend(["R", "R", "R", "P"])
        r -= 3
        p -= 1

    # gap-bridge pairing if we have left-over Ss
    assert r <= 2
    if r >= 2 and s > 1:
        assert p > 0
        pairing.extend(["R", "S", "R", "P"])
        r -= 2
        p -= 1
        s -= 1

    # pair remaining Rs with Ps
    while r > 0:
        assert p > 0
        pairing.extend(["R", "P"])
        r -= 1
        p -= 1

    # pair remaining Ss
    at_least_one_s = s >= 2
    while s > 0:
        pairing.append("S")
        s -= 1

        if p > 0:
            at_least_one_s = True
            pairing.append("P")
            p -= 1

    assert at_least_one_s

    # pair left-over Ps, if any
    while p > 0:
        pairing.append("P")
        p -= 1

    assert r == 0 and p == 0 and s == 0
    return pairing


def _verify_pairing(tournament):
    num_rounds = 0
    while num_rounds < 2:
        tournament = _reduce_tournament(tournament)
        num_rounds += 1

    num_r = tournament.count("R")
    num_s = tournament.count("S")
    return num_r == 0 and num_s >= 1


def _get_winner(a, b):
    if a == b:
        return a
    elif BEATS[a] == b:
        return a
    elif BEATS[b] == a:
        return b


@collecting
def _reduce_tournament(tournament):
    if len(tournament) == 1:
        yield tournament[0]
        return

    for i in range(0, len(tournament), 2):
        a = tournament[i]
        b = tournament[i + 1]
        winner = _get_winner(a, b)
        yield winner
