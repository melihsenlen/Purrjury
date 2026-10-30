import pytest

from purrjury.engine.generator import assign_statements
from purrjury.board.world import make_world
from tests.helpers import all_cats, fits, random_grid


@pytest.mark.parametrize("rows, cols, n_liars", [(2, 2, 1), (2, 3, 2), (3, 3, 3), (5, 5, 8)])
def test_every_cat_gets_a_fitting_statement(rows, cols, n_liars):
    for _ in range(100):
        grid = random_grid(rows, cols)
        world = make_world(rows * cols, n_liars)
        assign_statements(grid, world)
        for cat in all_cats(grid):
            assert cat.statement is not None
            assert cat.statement.speaker == cat.index
            assert fits(cat.statement, world, grid)


@pytest.mark.parametrize("rows, cols", [(2, 2), (3, 3), (4, 4)])
def test_no_two_cats_say_the_same_thing(rows, cols):
    for _ in range(50):
        grid = random_grid(rows, cols)
        world = make_world(rows * cols, (rows * cols) // 3)
        assign_statements(grid, world)
        keys = [cat.statement.key() for cat in all_cats(grid)]
        assert len(keys) == len(set(keys))


def test_cat_sounds_match_the_mood_and_keep_the_clue(monkeypatch):
    """Every clue gets a sound (chance 1), from the list for its mood, and the clue itself stays the same."""
    from purrjury import texts
    from purrjury.engine import generator
    monkeypatch.setattr(generator, "SOUND_CHANCE", 1.0)
    for _ in range(20):
        grid = random_grid(3, 3)
        world = make_world(9, 3)
        assign_statements(grid, world)
        before = {cat.index: cat.statement.to_text() for cat in all_cats(grid)}
        generator.add_cat_sounds(grid)
        for cat in all_cats(grid):
            text = cat.statement.to_text()
            sounds = texts.CAT_SOUNDS[cat.statement.mood()]
            assert any(text == f"{s} {before[cat.index]}" or text == f"{before[cat.index]} {s}" for s in sounds), text


def test_moods():
    from purrjury.statements import CountLiars, PairStatement
    assert CountLiars(0, [1], "", "exactly", 1).mood() == "angry"     # "Felix is a liar"
    assert CountLiars(0, [1], "", "exactly", 0).mood() == "happy"     # "Felix is honest"
    assert CountLiars(0, [1, 2, 3], "", "exactly", 1).mood() == "neutral"
    assert PairStatement(0, 1, 2, "both_liars").mood() == "angry"
    assert PairStatement(0, 1, 2, "both_honest").mood() == "happy"
    assert PairStatement(0, 1, 2, "same").mood() == "neutral"


def test_vary_wordings_never_repeats_a_pun_or_a_sound(monkeypatch):
    """With a sound on every clue and many "is honest" clues, the pass still leaves no pun and no sound twice."""
    import re
    from purrjury import texts
    from purrjury.engine import generator
    monkeypatch.setattr(generator, "SOUND_CHANCE", 1.0)
    puns = [re.sub(r"\{\w+\}", "", w) for wordings in generator._wording_lists() for w in wordings[1:]]
    sounds = [s for mood in texts.CAT_SOUNDS.values() for s in mood]
    for _ in range(30):
        grid = random_grid(4, 4)
        world = make_world(16, 5)
        assign_statements(grid, world)
        generator.add_cat_sounds(grid)
        before = [cat.statement.key() for cat in all_cats(grid)]
        generator.vary_wordings(grid)
        read = [cat.statement.text for cat in all_cats(grid) if not cat.hidden]
        for piece in puns + sounds:
            assert sum(piece in text for text in read) <= 1, piece
        assert [cat.statement.key() for cat in all_cats(grid)] == before   # the logic didn't change


def test_vary_wordings_keeps_the_names():
    from purrjury.engine import generator
    grid = random_grid(1, 3)
    for cat, about in zip(grid[0], ["Bean", "Cleo", "Dot"]):
        cat.statement = type("Clue", (), {})()
        cat.statement.text = f"{about} is honest, fur real."
    generator.vary_wordings(grid)
    assert [cat.statement.text for cat in grid[0]] == [
        "Bean is honest, fur real.", "Cleo is pawsitively honest.", "Dot is honest. That's a purr-fact."]
