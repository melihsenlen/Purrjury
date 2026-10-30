"""Tests for solver.py: the human-style step solver."""
import random

import pytest

from purrjury.engine.generator import generate_puzzle
from purrjury.engine.solver import levels_for, solve


@pytest.mark.parametrize("size", [3, 4])
def test_solver_finds_the_real_answer(size):
    """Whenever the solver gets through a puzzle, every cat it found matches the real world."""
    for seed in range(5):
        random.seed(seed)
        result = generate_puzzle(size, size, size * size // 3)
        if result is None:
            continue
        grid, world = result
        steps = solve(grid)
        if steps is None:
            continue   # stuck puzzles are allowed, they just get no rating
        known = {}
        for _level, _speakers, found, options in steps:
            assert options >= 1
            known.update(found)
        assert known == {i: world[i] for i in range(size * size)}


def test_levels_for_shifts_up_on_big_grids():
    assert levels_for(3, 3) == ["easy", "medium", "hard"]
    assert levels_for(4, 4) == ["medium", "hard", "tricky"]
