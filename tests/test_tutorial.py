"""Tests for tutorial.py: the "How to play" lessons."""
import pytest

from purrjury.engine.solver import forced_cats
from tutorial import build, lesson_chain, lesson_honest, lesson_liar


@pytest.fixture(scope="module")
def lessons():
    return build()   # also raises if a lesson has more than one answer or can't be solved


def test_five_lessons_in_order(lessons):
    assert [l["title"] for l in lessons] == [
        "Honest cats tell the truth", "Liars never tell the truth", "One cat leads to the next",
        "Your tools", "Your turn",
    ]


def test_why_lines_cover_every_cat_you_can_get_wrong_in_the_first_lessons():
    """Lessons 1 to 3 explain every wrong mark: every cat except the given one has a why line."""
    for maker in (lesson_honest, lesson_liar, lesson_chain):
        grid, _world, given, lesson = maker()
        cats = range(len(grid) * len(grid[0]))
        assert set(lesson["why"]) == {cat for cat in cats if cat not in given}


def test_after_points_at_other_cats_that_are_not_given():
    """lesson["after"]: a why line builds on other cats, which the player has to solve first (so not given ones)."""
    for maker in (lesson_honest, lesson_liar, lesson_chain):
        grid, _world, given, lesson = maker()
        for cat, first in lesson.get("after", {}).items():
            assert cat in lesson["why"]
            assert first and cat not in first
            assert not set(first) & set(given)


def test_tools_lesson_lists_the_three_tools(lessons):
    assert [task["id"] for task in lessons[3]["tasks"]] == ["used", "notes", "connections"]


def test_last_lesson_has_one_way_through_and_its_steps_follow_it(lessons):
    """At every step exactly one clue works, and it's the clue the step text points at."""
    from tutorial import lesson_your_turn
    grid, world, given, lesson, _seed = lesson_your_turn()
    clues = [cat.statement for row in grid for cat in row]
    known = dict(given)
    for step in lesson["steps"]:
        working = [clue for clue in clues if forced_cats([clue], known, grid)]
        assert [clue.speaker for clue in working] == [step["speaker"]]
        assert step["speaker"] != step["cat"]   # always about another cat
        assert forced_cats(working, known, grid) == {step["cat"]: world[step["cat"]]}
        known[step["cat"]] = world[step["cat"]]
    assert len(known) == 9


def test_generated_lessons_use_simple_clues_only(lessons):
    texts = [cat["text"] for lesson in lessons[3:] for cat in lesson["puzzle"]["cats"]]
    assert not any(text.startswith("At least one of these is true") for text in texts)
