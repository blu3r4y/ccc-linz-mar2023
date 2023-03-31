from typing import Iterable, NamedTuple, Tuple, List, Optional
import itertools

R, P, S = 0, 1, 2

Branch = NamedTuple(
    "Branch",
    [("r", int), ("p", int), ("s", int), ("goal", int)],
)

PARENTS = {}


def dfs(start: Branch, depth: int):
    if depth == 0:
        return start

    for left, right in successors(start):
        go_left = dfs(left, depth - 1)
        go_right = dfs(right, depth - 1)
        if go_left is not None and go_right is not None:
            return left, right


def backtrace_to_root(state: Branch):
    path = [state]
    while state in PARENTS:
        state = PARENTS[state]
        path.append(state)
    return path


def successors(state: Branch) -> Iterable[Tuple[Branch, Branch]]:
    r, p, s = state.r, state.p, state.s

    # the duplication step is always an option
    if state.goal == R and r >= 2:
        for a, b in distribute_players((r, p, s), (R, R)):
            yield a, b
    elif state.goal == P and p >= 2:
        for a, b in distribute_players((r, p, s), (P, P)):
            yield a, b
    elif state.goal == S and s >= 2:
        for a, b in distribute_players((r, p, s), (S, S)):
            yield a, b

    # otherwise, we need to eliminate another player
    if state.goal == R and s >= 1:  # eliminate S
        for a, b in distribute_players((r, p, s), (R, S), (1, 0, 1)):
            if a.r >= 1 and b.s >= 1:
                yield a, b
    elif state.goal == S and p >= 1:  # eliminate P
        for a, b in distribute_players((r, p, s), (S, P), (0, 1, 1)):
            if a.s >= 1 and b.p >= 1:
                yield a, b
    elif state.goal == P and r >= 1:  # eliminate R
        for a, b in distribute_players((r, p, s), (P, R), (1, 1, 0)):
            if a.p >= 1 and b.r >= 1:
                yield a, b


def distribute_players(
    players: Tuple[int],
    goals: Tuple[int],
    minima: Optional[Tuple[int]] = None,
) -> Iterable[Tuple[Branch, Branch]]:
    assert sum(players) % 2 == 0, "uneven number of players"

    ranges = [range(p + 1) for p in players]
    for cnt_left in itertools.product(*ranges):
        cnt_right = tuple(p - c for p, c in zip(players, cnt_left))

        # ensure balanced tree
        if sum(cnt_left) != sum(cnt_right):
            continue

        # ensure minimal players in at least one branch
        if minima is not None and not all(
            (cl >= m or cr >= m) for cl, cr, m in zip(cnt_left, cnt_right, minima)
        ):
            continue

        # ensure that both branches can satisfy the goals
        goal_a, goal_b = goals
        is_goal_a_left = cnt_left[goal_a] >= (minima[goal_a] if minima else 0)
        is_goal_b_right = cnt_right[goal_b] >= (minima[goal_b] if minima else 0)
        if is_goal_a_left != is_goal_b_right:
            continue

        # possibly swap branches
        if not is_goal_a_left:
            cnt_left, cnt_right = cnt_right, cnt_left

        yield Branch(*cnt_left, goal_a), Branch(*cnt_right, goal_b)


def determine_two_rounded_pairings(r, p, s):
    """
    Generates correct pairing for when only
    two rounds of the tournament are played.
    """
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
