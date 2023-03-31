from .generation import determine_two_rounded_pairings
from .playing import play_rounds, play_tournament


def solve(data):
    result = []
    for exp in data["expected"]:
        tournament = determine_two_rounded_pairings(exp.r, exp.p, exp.s)
        assert verify_tournament(tournament, after_two_rounds=True)
        result.append("".join(tournament))

    return "\n".join(result)


def verify_tournament(tournament, after_two_rounds=False):
    if after_two_rounds:
        tournament = play_rounds(tournament, rounds=2)
        num_r = tournament.count("R")
        num_s = tournament.count("S")
        return num_r == 0 and num_s >= 1

    tournament = play_tournament(tournament)
    return tournament == "S"
