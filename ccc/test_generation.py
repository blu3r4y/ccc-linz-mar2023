from .generation import (
    distribute_players,
    successors,
    dfs,
    Branch,
    backtrace_to_root,
    R,
    P,
    S,
)


def test_distribute_1r1p0s():
    pairings = list(distribute_players((1, 1, 0), goals=(R, P)))
    assert (Branch(1, 0, 0, R), Branch(0, 1, 0, P)) in pairings


def test_distribute_2r2p0s():
    pairings = list(distribute_players((2, 2, 0), goals=(R, R)))
    assert (Branch(2, 0, 0, R), Branch(0, 2, 0, R)) in pairings
    assert (Branch(1, 1, 0, R), Branch(1, 1, 0, R)) in pairings


def test_distribute_2r2p2s():
    pairings = list(distribute_players((2, 2, 2), goals=(R, R)))
    assert (Branch(2, 0, 1, R), Branch(0, 2, 1, R)) in pairings
    assert (Branch(0, 2, 1, R), Branch(2, 0, 1, R)) in pairings
    assert (Branch(2, 1, 0, R), Branch(0, 1, 2, R)) in pairings
    assert (Branch(0, 1, 2, R), Branch(2, 1, 0, R)) in pairings
    assert (Branch(1, 2, 0, R), Branch(1, 0, 2, R)) in pairings
    assert (Branch(1, 1, 1, R), Branch(1, 1, 1, R)) in pairings


def test_successors_2s():
    state = Branch(3, 1, 0, P)
    succ = list(successors(state))


def test_dfs():
    start = Branch(4, 3, 1, S)
    result = dfs(start, depth=3)
    trace = backtrace_to_root(result)
    print(result)
    print(trace)
