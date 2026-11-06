"""Tests for the path-based generator: no big reveals, few choices per step, a varied clue mix."""
import random
from collections import Counter

import pytest

from purrjury.engine.checker import find_solutions
from purrjury.engine.path_generator import (KIND_SHARE, KIND_SHARE_OVERRIDES, PathSettings, check_puzzle,
                                            generate_path_puzzle)
from purrjury.engine.solver import forced_cats, solve
from purrjury.statements import CountLiars
from tests.helpers import fixed_grid, is_honest, is_liar


def make(rows, cols, settings, seed):
    random.seed(seed)
    result = generate_path_puzzle(rows, cols, rows * cols // 3, settings)
    assert result is not None
    return result


def all_clues(grid):
    return [cat.statement for row in grid for cat in row if not cat.hidden]


# --- the finished puzzles ---

@pytest.mark.parametrize("seed", range(5))
def test_path_puzzle_has_one_answer_and_it_is_the_world(seed):
    grid, world, steps, given = make(3, 3, PathSettings(openers=2), seed)
    assert find_solutions(grid) == [tuple(world)]
    known = dict(given)
    for _level, _speakers, found, _options in steps:
        known.update(found)
    assert known == {i: world[i] for i in range(9)}


@pytest.mark.parametrize("rows, cols, cap, seed", [(3, 3, 1, 0), (3, 3, 1, 1), (3, 3, 2, 2), (4, 4, 1, 3)])
def test_no_clue_reveals_too_much_before_the_endgame(rows, cols, cap, seed):
    """Not just the solver's pick: EVERY clue that works at a step stays within the cap."""
    settings = PathSettings(openers=2, max_cats_per_step=cap)
    grid, _world, steps, given = make(rows, cols, settings, seed)
    known = dict(given)
    for _level, _speakers, found, options in steps:
        if len(known) < settings.endgame * rows * cols:
            assert options <= settings.max_choices
            for clue in all_clues(grid):
                assert len(forced_cats([clue], known, grid)) <= cap
        known.update(found)


@pytest.mark.parametrize("openers, seed", [(1, 0), (1, 1), (2, 2)])
def test_openers_stay_within_the_setting(openers, seed):
    grid, _world, _steps, _given = make(3, 3, PathSettings(openers=openers), seed)
    working = [clue for clue in all_clues(grid) if forced_cats([clue], {}, grid)]
    assert 1 <= len(working) <= openers


def test_given_cat_is_shown_with_its_real_type():
    grid, world, steps, given = make(3, 3, PathSettings(given=True), 4)
    assert len(given) == 1
    cat, is_liar_value = next(iter(given.items()))
    assert world[cat] == is_liar_value
    assert solve(grid, given) == steps


@pytest.mark.parametrize("rows, cols, seed", [(3, 3, 0), (3, 3, 1), (3, 3, 2), (4, 4, 3)])
def test_shown_cats_own_clue_finds_a_cat_right_away(rows, cols, seed):
    """A new player reads the shown cat's clue first, so with only that cat known, its clue already finds another."""
    grid, world, _steps, given = make(rows, cols, PathSettings(given=True, max_cats_per_step=2), seed)
    (cat, _is_liar), = given.items()
    found = forced_cats([grid[cat // cols][cat % cols].statement], given, grid)
    assert found and all(world[c] == value for c, value in found.items())


@pytest.mark.parametrize("rows, cols, seed", [(3, 3, 5), (3, 3, 6), (4, 4, 7)])
def test_clue_mix_keeps_every_kind_within_its_share(rows, cols, seed):
    grid, _world, _steps, _given = make(rows, cols, PathSettings(openers=2), seed)
    n_cats = rows * cols
    for kind, used in Counter(clue.kind() for clue in all_clues(grid)).items():
        assert used <= max(1, round(n_cats * KIND_SHARE_OVERRIDES.get(kind, KIND_SHARE))), kind


@pytest.mark.parametrize("rows, cols, most", [(3, 3, 1), (4, 4, 2)])
def test_either_or_and_connected_clues_are_rare(rows, cols, most):
    """At most 1 either/or per puzzle, and at most 1 connected clue on a 3x3 (2 on a 4x4)."""
    for seed in range(5 if rows == 3 else 2):
        grid, _world, _steps, _given = make(rows, cols, PathSettings(openers=2), seed)
        kinds = [clue.kind() for clue in all_clues(grid)]
        assert kinds.count("either_or") <= 1
        assert kinds.count("next_to") <= most


# --- check_puzzle on a hand-made puzzle ---

def big_reveal_puzzle():
    """A 2x2 where, with cat 0 shown as honest, cat 0's clue reveals cats 1 and 2 at once.

    0 1      world: only cat 3 is a liar
    2 3
    """
    grid = fixed_grid(2, 2)
    grid[0][0].statement = CountLiars(0, [1, 2], "", "exactly", 0)   # "1 and 2 are honest"
    grid[0][1].statement = is_liar(1, 3)
    grid[1][0].statement = is_honest(2, 0)
    grid[1][1].statement = is_liar(3, 0)                            # a lie: 0 is honest
    given = {0: False}
    return grid, given


def test_check_puzzle_catches_a_big_reveal_the_solver_did_not_pick():
    grid, given = big_reveal_puzzle()
    steps = solve(grid, given)
    assert check_puzzle(grid, steps, PathSettings(max_cats_per_step=1), given) is False
    assert check_puzzle(grid, steps, PathSettings(max_cats_per_step=2), given) is True


def test_check_puzzle_catches_too_many_choices():
    grid, given = big_reveal_puzzle()
    steps = solve(grid, given)
    assert steps[0][3] == 3   # clues of 0, 2 and 3 all work at the start
    assert check_puzzle(grid, steps, PathSettings(max_cats_per_step=2, max_choices=2), given) is False


def test_check_puzzle_has_no_limits_in_the_endgame():
    grid, given = big_reveal_puzzle()
    steps = solve(grid, given)
    assert check_puzzle(grid, steps, PathSettings(max_cats_per_step=1, endgame=0.25), given) is True


def test_check_puzzle_rejects_a_stuck_puzzle():
    assert check_puzzle(fixed_grid(2, 2), None, PathSettings(), {}) is False
