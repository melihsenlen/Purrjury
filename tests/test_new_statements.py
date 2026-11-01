"""Tests for Compare, OddLiars, NextToEachOther, "Bean's neighbors" areas, kinds and the whole-grid cleanup."""
import pytest

from purrjury.board import areas
from purrjury.board.world import make_world
from purrjury.statements import (ALL_STATEMENTS, AllSame, Compare, CountLiars, IfThen, NextToEachOther,
                                 OddLiars, Only, PairStatement)
from purrjury.statements.count_liars import EVERYONE_TEXT
from purrjury.statements.next_to import one_group
from tests.helpers import fixed_grid, random_grid


# --- Compare ---

def test_compare_evaluate():
    world = [True, True, False, True, False, False]   # 2x3: row 1 has 2 liars, row 2 has 1
    row1, row2 = [0, 1, 2], [3, 4, 5]
    assert Compare(0, row1, "", row2, "", "more_liars").evaluate(world, None) is True
    assert Compare(0, row2, "", row1, "", "more_liars").evaluate(world, None) is False
    assert Compare(0, row2, "", row1, "", "more_honest").evaluate(world, None) is True
    assert Compare(0, row1, "", row2, "", "same_liars").evaluate(world, None) is False
    assert Compare(0, [0, 3], "", [1, 2], "", "same_liars").evaluate(world, None) is False
    assert Compare(0, [0, 2], "", [1, 4], "", "same_liars").evaluate(world, None) is True


def test_compare_more_honest_counts_honest_cats_not_fewer_liars():
    """A big area can have more liars AND more honest cats than a small one."""
    world = [True, False, False, True, False]
    big, small = [0, 1, 2, 3], [4]
    assert Compare(0, big, "", small, "", "more_liars").evaluate(world, None) is True
    assert Compare(0, big, "", small, "", "more_honest").evaluate(world, None) is True


def test_compare_key_order_only_matters_for_more():
    a, b = [0, 1], [2, 3]
    assert Compare(0, a, "", b, "", "same_liars").key() == Compare(5, b, "", a, "", "same_liars").key()
    assert Compare(0, a, "", b, "", "more_liars").key() != Compare(0, b, "", a, "", "more_liars").key()


def test_compare_random_never_compares_an_area_with_itself():
    for _ in range(100):
        grid = random_grid(3, 3)
        world = make_world(9, 3)
        for speaker in range(9):
            s = Compare.random(speaker, grid, world)
            if s is not None:
                assert set(s.area_a) != set(s.area_b)
                assert len(s.area_a) >= 2 and len(s.area_b) >= 2


# --- OddLiars ---

def test_odd_evaluate():
    world = [True, False, True, True]
    assert OddLiars(0, [0, 1], "").evaluate(world, None) is True      # 1 liar
    assert OddLiars(0, [0, 2], "").evaluate(world, None) is False     # 2 liars
    assert OddLiars(0, [1], "").evaluate(world, None) is False        # 0 liars is even
    assert OddLiars(0, [0, 2, 3], "").evaluate(world, None) is True   # 3 liars


def test_there_is_no_even_wording():
    """Only "odd": with "even" players would wonder whether 0 counts."""
    from purrjury import texts
    for name in dir(texts):
        value = getattr(texts, name)
        if name.isupper() and isinstance(value, list):
            assert not any("even" in text.lower().split() for text in value), name


# --- NextToEachOther ---

def test_one_group_in_a_row_means_side_by_side():
    grid = fixed_grid(1, 4)
    assert one_group([1, 2], grid)
    assert one_group([0, 1, 2], grid)
    assert not one_group([0, 2], grid)      # a gap in between
    assert not one_group([0, 1, 3], grid)


def test_one_group_on_the_grid_walks_around_corners_but_not_diagonals():
    grid = fixed_grid(3, 3)   # 0 1 2 / 3 4 5 / 6 7 8
    assert one_group([0, 3, 4, 5], grid)    # an L shape
    assert not one_group([0, 4], grid)      # diagonal only
    assert not one_group([0, 1, 7, 8], grid)


def test_next_to_needs_two_or_more():
    grid = fixed_grid(1, 4)
    row = [0, 1, 2, 3]
    assert NextToEachOther(0, row, "Row 1", True).evaluate([False, False, False, False], grid) is False   # 0
    assert NextToEachOther(0, row, "Row 1", True).evaluate([False, True, False, False], grid) is False    # 1 liar
    assert NextToEachOther(0, row, "Row 1", True).evaluate([False, True, True, False], grid) is True
    assert NextToEachOther(0, row, "Row 1", True).evaluate([True, False, True, False], grid) is False    # split
    assert NextToEachOther(0, row, "Row 1", False).evaluate([True, False, False, True], grid) is True    # honest


def test_next_to_lie_means_fewer_than_two_or_split():
    """The text says "2 or more", so a liar saying it can mean 0 or 1 of them, or split up."""
    grid = fixed_grid(1, 4)
    row = [0, 1, 2, 3]
    clue = NextToEachOther(0, row, "My row", True)
    assert clue.fits([True, True, False, False], grid) is False    # 0 and 1 connected: a liar can't say it
    assert clue.fits([True, False, True, False], grid) is True     # split: a liar can say it
    assert clue.fits([True, False, False, False], grid) is True    # only 1 liar (the speaker): a liar can say it
    assert clue.fits([False, True, True, False], grid) is True     # honest speaker, 1 and 2 connected
    assert clue.fits([False, False, False, False], grid) is False  # no liars: an honest cat can't say it


def test_next_to_texts():
    grid = fixed_grid(3, 3)
    s = NextToEachOther(0, [0, 1, 2], "My row", True)
    s.set_text(grid)
    assert s.to_text() == "My row has 2 or more liars, all connected."
    s = NextToEachOther(0, areas.everyone(grid), None, False)
    s.set_text(grid)
    assert s.to_text() == "There are 2 or more honest cats, all connected."


# --- "Bean's neighbors" areas ---

def test_their_neighbors_areas_match_the_name():
    grid = random_grid(3, 3)
    candidates = CountLiars.candidate_areas(grid, 0)
    names = {cat.name: cat for row in grid for cat in row}
    assert candidates["theirs"]
    for area, text in candidates["theirs"]:
        cat = names[text.removesuffix("'s neighbors")]
        assert area == areas.neighbors(grid, cat)
        assert cat.index != 0


# --- Kinds ---

def test_kinds():
    assert CountLiars(0, [1], "", "exactly", 1).kind() == "is"
    assert CountLiars(0, [1, 2], "my neighbors", "exactly", 1).kind() == "count"
    assert CountLiars(0, list(range(9)), EVERYONE_TEXT, "exactly", 3).kind() == "total"
    assert PairStatement(0, 1, 2, "if_a_honest_then_b").kind() == "either_or"
    assert PairStatement(0, 1, 2, "both_liars").kind() == "pair"
    assert IfThen(0, 5, True, [0, 1], "", False).kind() == "either_or"
    assert AllSame(0, [0, 4], "", True).kind() == "all_same"
    assert Only(0, [0, 1], "", 1, True).kind() == "only"


# --- The whole grid is only for counts ---

@pytest.mark.parametrize("rows, cols", [(2, 3), (3, 3)])
def test_only_counts_and_next_to_use_the_whole_grid(rows, cols):
    """'All the cats are the same' and friends are always settled, so only counts may cover every cat.

    NextToEachOther is the exception: "all the liars are in one group" can go either way.
    """
    n_cats = rows * cols
    for _ in range(30):
        grid = random_grid(rows, cols)
        world = make_world(n_cats, n_cats // 3)
        for speaker in range(n_cats):
            for statement_type in (Only, AllSame, IfThen, OddLiars):
                s = statement_type.random(speaker, grid, world)
                if s is not None:
                    assert len(set(s.area)) < n_cats, s.to_text()


def test_total_counts_are_never_settled_from_the_start():
    """No "exactly 0", "exactly all" or "at least 1" in total: every puzzle has both types."""
    for _ in range(200):
        grid = random_grid(3, 3)
        world = make_world(9, 3)
        for speaker in range(9):
            s = CountLiars.random(speaker, grid, world)
            if s.kind() == "total":
                assert 1 <= s.n <= 8
                if s.mode == "at_least":
                    assert s.n >= 2


@pytest.mark.parametrize("statement_type", ALL_STATEMENTS)
def test_every_statement_type_has_its_own_kind(statement_type):
    """kind() never falls back to the class name for the clue types players see."""
    grid = random_grid(3, 3)
    for _ in range(20):
        world = make_world(9, 3)
        s = statement_type.random(0, grid, world)
        if s is not None:
            assert s.kind() in {"is", "count", "total", "pair", "either_or", "only", "all_same", "compare", "odd", "next_to", "individualist"}