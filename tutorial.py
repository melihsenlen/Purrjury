"""Build the "How to play" lessons and save them for the web version (web/tutorial.js).

Lessons 1 to 3 are tiny hand-made puzzles, lessons 4 and 5 come from the path generator with
fixed seeds and simple clues only. Lesson 5 is a strict chain: exactly one clue works at every
step, so its "Next step" help can walk you through it one clue at a time.
Run it again after changing a lesson: python tutorial.py
"""
import json
import random

from export import has_trick_clue, puzzle_to_dict
from purrjury.board.cat import Cat
from purrjury.engine.checker import find_solutions
from purrjury.engine.path_generator import PathSettings, generate_path_puzzle
from purrjury.engine.solver import solve
from purrjury.statements import CountLiars, Only, PairStatement

# Lessons 4 and 5 only use the clues a beginner reads at a glance
SIMPLE_CLUES = (CountLiars, PairStatement, Only)

# One way through: one cat per clue, one working clue at a time, and no easier ending.
# shown_first=False keeps lessons 4 and 5 as they were made (their seeds and texts were picked by hand)
STRICT = PathSettings(max_cats_per_step=1, max_choices=1, endgame=1.0, openers=1, given=True,
                      shown_first=False, clue_types=SIMPLE_CLUES)

# Lessons 4 and 5 try seeds from here until one works, so every run makes the same lessons.
# 1434 is the first seed from 500 on that gives lesson 5 (the search took 4 minutes, so it starts there now)
FIRST_SEED = {4: 400, 5: 1434}


def hand_grid(cats):
    """A grid from a list of rows, each row a list of (name, color). Statements are added after."""
    grid, index = [], 0
    for r, row in enumerate(cats):
        grid.append([])
        for c, (name, color) in enumerate(row):
            grid[r].append(Cat(name, r, c, index, color))
            index += 1
    return grid


def say(grid, index, statement, text):
    """Give a cat its clue, with an exact text (so no random pun or cat sound sneaks into a lesson)."""
    statement.set_text(grid)
    statement.text = text
    grid[index // len(grid[0])][index % len(grid[0])].statement = statement


def lesson_honest():
    """1: Ash is given as honest, so Ash's clue is simply true."""
    grid = hand_grid([[("Ash", "orange"), ("Bean", "black")]])
    say(grid, 0, CountLiars(0, [1], "", "exactly", 1), "Bean is a liar.")
    say(grid, 1, CountLiars(1, [0], "", "exactly", 1), "Ash is a liar.")
    return grid, [False, True], {0: False}, {
        "title": "Honest cats tell the truth",
        # "corner", not "bottom right": on phones the lock sits top right, on the name band
        "intro": "Ash is honest: the \U0001F512 in the corner of Ash's card means it's given. So Ash's clue is true. "
                 "Tap Bean to mark it: once for honest, twice for liar.",
        "why": {1: "Ash is honest, so Ash's clue is true: Bean is a liar."},
        "done": "Right! And Bean's clue is false, just like a liar's clue should be.",
    }


def lesson_liar():
    """2: nothing given. Ash can't be honest, because then Ash would be a liar."""
    grid = hand_grid([[("Ash", "white"), ("Bean", "grey")]])
    say(grid, 0, PairStatement(0, 0, 1, "both_liars"), "Bean and I are both liars.")
    say(grid, 1, CountLiars(1, [0], "", "exactly", 1), "Ash is a liar.")
    return grid, [True, False], {}, {
        "title": "Liars never tell the truth",
        "intro": "Nothing is given this time. Try both options for Ash: could Ash be honest?",
        "why": {
            0: "If Ash were honest, Ash's clue would be true, and then Ash would be a liar. So Ash is a liar.",
            1: "Ash is a liar, so Ash's clue is false: at least one of them is honest. That's Bean.",
        },
        # Bean's why line builds on Ash: tapping Bean first makes the guide say to start with Ash
        "after": {1: [0]},
        # once Ash is right, the guide points at Bean (a nudge, not the answer)
        "next": {1: "Right, Ash is a liar! So Ash's clue is false. What does that tell you about Bean?"},
        "done": "That's the whole trick: a liar's clue is always false.",
    }


def lesson_chain():
    """3: one solved cat tells you how to read its clue, which solves the next cat."""
    grid = hand_grid([[("Ash", "yellow"), ("Bean", "brown"), ("Cleo", "orange")]])
    say(grid, 0, CountLiars(0, [1], "", "exactly", 1), "Bean is a liar.")
    say(grid, 1, CountLiars(1, [2], "", "exactly", 0), "Cleo is honest.")
    say(grid, 2, CountLiars(2, [0], "", "exactly", 1), "Ash is a liar.")
    return grid, [False, True, True], {0: False}, {
        "title": "One cat leads to the next",
        "intro": "Solve one cat, then use its clue to solve the next. A liar's clue is false, so flip it.",
        "why": {
            1: "Ash is honest, so Bean is a liar.",
            2: "Bean is a liar, so Bean's clue is false: Cleo is a liar too.",
        },
        "after": {2: [1]},
        "next": {2: "Right, Bean is a liar! So flip Bean's clue. What does it tell you about Cleo?"},
        "done": "That's chaining: every cat you solve tells you how to read its clue.",
    }


def beginner_friendly(grid, steps, others_only):
    """No trick clues and no either/or. With others_only, every step reveals a cat other than the speaker:
    "I'm the only liar among ..." about yourself is the hardest kind of reasoning for a beginner."""
    if has_trick_clue(grid):
        return False
    if any(cat.statement.kind() == "either_or" for row in grid for cat in row):
        return False
    if others_only and any(speakers[0] in found for _level, speakers, found, _options in steps):
        return False
    return True


def generated(rows, cols, n_liars, lesson, others_only=False):
    """The first strict, beginner-friendly puzzle from FIRST_SEED on: (grid, world, steps, given, seed)."""
    seed = FIRST_SEED[lesson]
    while True:
        random.seed(seed)
        result = generate_path_puzzle(rows, cols, n_liars, STRICT)
        if result is not None and beginner_friendly(result[0], result[2], others_only):
            return (*result, seed)
        seed += 1


def lesson_tools():
    """4: a 2x2 where the guide walks you through the tools one step at a time (lesson["tour"]).
    The texts are written for this exact puzzle (seed 400): Apricot, Biscuit, Clover, Doodle, Doodle given."""
    grid, world, _steps, given, seed = generated(2, 2, 1, 4)
    return grid, world, given, {
        "title": "Your tools",
        "intro": "A tiny puzzle to try the buttons on. I'll show you each one.",
        # Each step points at a button or a cat and is done once you've done it ("done").
        # The guide shows the first step that isn't done, so doing one early just skips it later.
        # {press} becomes "Right click" on a computer and "Long-press" on a phone.
        "tour": [
            {"id": "note", "point": "pen", "cat": 3, "done": {"note": 3},
             "text": "Doodle is honest, so its clue is true. Tap ✎ on Doodle and write that down in your own words. "
                     "You can add a tag there too.",
             "placeholder": "e.g. one of Biscuit and Clover is a liar"},
            {"id": "connections", "point": "card", "cat": 3, "done": {"connections": 3},
             "text": "{press} Doodle to see which cats talk about Doodle."},
            {"id": "clover", "point": "card", "cat": 2, "done": {"mark": [2, "honest"]},
             "text": "Clover talks about Doodle: \"Doodle is honest.\" That's true, so Clover is honest too. Mark Clover."},
            {"id": "hint", "point": "hint", "done": {"mark": [1, "liar"]},
             "text": "Who's next? Press Hint to see a clue that works right now.",
             "again": "That's Doodle's clue. Press Hint again to see which cat it finds.",
             "found": "Doodle's clue finds Biscuit: one of Biscuit, Clover and Doodle is a liar, "
                      "and it's not Clover or Doodle. Mark Biscuit."},
            {"id": "used", "point": "check", "cat": 3, "done": {"used": 3},
             "text": "Doodle's clue is used up. Tap its ✓ to grey it out. "
                     "Clover's and Biscuit's are used up too, grey them out if you like."},
            {"id": "last", "text": "Figure out Apricot yourself now!"},
        ],
        "why": {
            0: "Biscuit is a liar, so Doodle is the only honest cat in column 2. Apricot's clue is true: Apricot is honest.",
            1: "Doodle is honest, so exactly one of Biscuit, Clover and Doodle is a liar. That's Biscuit.",
            2: "If Clover were a liar, Clover's clue would be false, and Doodle would be a liar. But Doodle is honest.",
        },
        "after": {0: [1], 1: [2]},
        "done": "Solved! Those tools are there in every puzzle, use them whenever they help.",
    }, seed


def lesson_your_turn():
    """5: a real easy 3x3 with only one way through, so Next step can always point at the one clue that works."""
    grid, world, steps, given, seed = generated(3, 3, 3, 5, others_only=True)
    names = [cat.name for row in grid for cat in row]
    walk = []
    for _level, speakers, found, _options in steps:
        (cat, is_liar), = found.items()
        walk.append({
            "speaker": speakers[0],
            "cat": cat,
            "text": f"Read {names[speakers[0]]}'s clue. Then {names[cat]} must be {'a liar' if is_liar else 'honest'}.",
        })
    return grid, world, given, {
        "title": "Your turn",
        # Cricket's clue is about Nimbus's neighbors, and players may count the corners too
        "intro": "A real puzzle. At every step exactly one clue helps. Stuck? Press Next step. "
                 "Neighbors are only the cats above, below, left and right, no corners.",
        "steps": walk,
        # no feedback on single marks here, only this once every cat is marked and the lesson isn't solved
        "off": "Something doesn't add up. Press Next step to find it.",
        # short, so it fits on one line with the "Back to the menu" button (the bubble keeps room for it)
        "done": "You solved a whole puzzle!",
    }, seed


def answers(grid, given):
    """Every answer that fits all clues and the cats shown from the start."""
    return [world for world in find_solutions(grid) if all(world[cat] == value for cat, value in given.items())]


def build():
    """All lessons as plain data for the web page, each checked for exactly one answer."""
    lessons = []
    makers = [lesson_honest, lesson_liar, lesson_chain, lesson_tools, lesson_your_turn]
    for number, maker in enumerate(makers, start=1):
        made = maker()
        grid, world, given, lesson = made[:4]
        seed = made[4] if len(made) > 4 else None
        if answers(grid, given) != [tuple(world)]:
            raise ValueError(f"lesson {number} doesn't have exactly one answer")
        if solve(grid, given) is None:
            raise ValueError(f"lesson {number} can't be solved one clue at a time")
        given_cat = next(iter(given)) if given else None
        lesson["puzzle"] = puzzle_to_dict(grid, world, seed, "lesson", given_cat)
        lessons.append(lesson)
    return lessons


def main():
    lessons = build()
    with open("web/tutorial.js", "w", encoding="utf-8") as f:
        f.write("// Made by tutorial.py, don't edit by hand\n")
        f.write("const LESSONS = " + json.dumps(lessons, indent=1) + ";\n")
    print(f"Saved {len(lessons)} lessons to web/tutorial.js")


if __name__ == "__main__":
    main()
