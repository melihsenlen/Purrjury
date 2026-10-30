"""Generate a batch of puzzles and save them for the web version (web/puzzles.js).

The web page can't read files on its own when you open it straight from disk,
so the puzzles are saved as a small JavaScript file that sets PUZZLES.
"""
import argparse
import base64
import json
import random
from datetime import datetime

from purrjury.engine.path_generator import PathSettings, generate_path_puzzle
from purrjury.engine.solver import BIG_GRID, LEVELS, involved, levels_for

# Give up on a level after this many seeds, in case its settings are too hard to fill
MAX_TRIES = 200

# Trick clues ("Felix and I are the same type") only appear in puzzles of this level and up
TRICK_MIN_LEVEL = "hard"

# What each level asks of the path generator (see PathSettings). Harder levels: clues reveal fewer cats
# at once, fewer clues work at the same time (more searching) and there are fewer ways in.
# Easy shows one cat from the start. Playtesting decides these, they're just a first guess.
LEVEL_SETTINGS = {
    "easy":   PathSettings(max_cats_per_step=2, max_choices=3, openers=1, given=True),
    "medium": PathSettings(max_cats_per_step=2, max_choices=3, openers=2),
    "hard":   PathSettings(max_cats_per_step=1, max_choices=2, openers=1),
}
# A big grid (BIG_GRID cats or more) is one level up, so it gets its own steps between medium and tricky
BIG_LEVEL_SETTINGS = {
    "medium": PathSettings(max_cats_per_step=2, max_choices=3, openers=2),
    "hard":   PathSettings(max_cats_per_step=1, max_choices=3, openers=2),
    "tricky": PathSettings(max_cats_per_step=1, max_choices=2, openers=1),
}


def liar_count(n_cats):
    """Any number of liars from 1 to all but one, mostly around a third to a half of the cats."""
    return max(1, min(n_cats - 1, round(random.triangular(1, n_cats - 1, n_cats * 0.4))))


def make_puzzle(rows, cols, level, seed):
    """The puzzle a seed makes for a level: (grid, world, steps, given), or None if it didn't work out.

    The same seed always makes the same puzzle, so a saved seed can be turned back into its puzzle.
    None also when a trick clue ends up in a level below TRICK_MIN_LEVEL.
    """
    random.seed(seed)
    settings = (BIG_LEVEL_SETTINGS if rows * cols >= BIG_GRID else LEVEL_SETTINGS)[level]
    result = generate_path_puzzle(rows, cols, liar_count(rows * cols), settings)
    if result is None:
        return None
    if LEVELS.index(level) < LEVELS.index(TRICK_MIN_LEVEL) and has_trick_clue(result[0]):
        return None
    return result


def has_trick_clue(grid):
    """True if a clue the player can read is a trick clue. Hidden cats' real clues can't be read, so they don't count."""
    return any(cat.statement.is_trick() for row in grid for cat in row if not cat.hidden)


def clue_table(statement, grid):
    """Everything the hint button needs to know about one clue, without knowing how clues work.

    Returns {"cats": [...], "table": "..."}: the cats the clue is about (speaker included), and
    for every honest/liar combination of those cats, whether the clue fits it. Combination k has
    cat number j as a liar if bit j of k is set. The fits are packed 8 per byte, then base64.
    """
    cats = sorted(involved(statement))
    n_cats = len(grid) * len(grid[0])
    bits = bytearray((2 ** len(cats) + 7) // 8)
    for k in range(2 ** len(cats)):
        world = [False] * n_cats   # cats outside the clue don't matter
        for j, cat in enumerate(cats):
            world[cat] = bool(k >> j & 1)
        if statement.fits(world, grid):
            bits[k // 8] |= 1 << (k % 8)
    return {"cats": cats, "table": base64.b64encode(bytes(bits)).decode()}


def puzzle_to_dict(grid, world, seed, level, given=None):
    """Turn a generated puzzle into plain data the web page can use."""
    cats = []
    for row in grid:
        for cat in row:
            cats.append({
                "name": cat.name,
                "color": cat.color,
                "row": cat.row,
                "column": cat.column,
                "text": cat.gibberish if cat.hidden else cat.statement.to_text(),
                "hidden": cat.hidden,
                "secret": cat.statement.to_text() if cat.hidden else None,   # shown after Reveal
                # the other cats this cat talks about. Hidden cats show none, that would give away their statement
                "mentions": [] if cat.hidden else cat.statement.mentions(),
                # which face the cat's sprite shows. Hidden cats only meow, so they look neutral
                "mood": "neutral" if cat.hidden else cat.statement.mood(),
                # for the hint button. Hidden cats' clues can't be used, so they have none
                "clue": None if cat.hidden else clue_table(cat.statement, grid),
            })
    return {
        "rows": len(grid),
        "cols": len(grid[0]),
        "seed": seed,
        "level": level,   # "easy", "medium", "hard" or "tricky", from the solver
        "given": given,   # index of a cat the page shows as solved from the start, or None
        "cats": cats,
        "liars": world,   # world[i] is True if cat i is a liar
    }


def export(sizes, count, path="web/puzzles.js", first_seed=None, max_tries=MAX_TRIES):
    """Generate count puzzles for every difficulty level of every size, and write them to path.

    Each level is built on purpose by the path generator with its own settings (LEVEL_SETTINGS),
    instead of making random puzzles and rating them afterwards.
    Returns the puzzles, sorted by size and then from easy to hard.
    """
    seed = first_seed if first_seed is not None else random.randrange(1_000_000)
    puzzles = []

    for rows, cols in sizes:
        for level in levels_for(rows, cols):
            made = 0
            # every puzzle gets its own seed so it can be made again (see make_puzzle)
            for _ in range(max_tries):
                if made == count:
                    break
                seed += 1
                result = make_puzzle(rows, cols, level, seed)
                if result is None:
                    continue
                grid, world, _steps, given = result
                given_cat = next(iter(given)) if given else None
                puzzles.append(puzzle_to_dict(grid, world, seed, level, given_cat))
                made += 1
            if made < count:
                print(f"Only found {made} {level} {rows}x{cols} puzzles, wanted {count}")

    with open(path, "w", encoding="utf-8") as f:
        f.write("// Made by export.py, don't edit by hand\n")
        # shown at the bottom of the page, so you can tell an old cached puzzles.js from the latest one
        f.write(f'const PUZZLES_MADE = "{datetime.now():%d %b %Y, %H:%M}";\n')
        f.write("const PUZZLES = " + json.dumps(puzzles, indent=1) + ";\n")
    return puzzles


def parse_size(text):
    """Turn "3x4" into (3, 4)."""
    rows, cols = text.lower().split("x")
    return int(rows), int(cols)


def main():
    """Read the arguments and export the puzzles."""
    parser = argparse.ArgumentParser(description="Export puzzles for the web version (web/puzzles.js).")
    parser.add_argument("sizes", nargs="*", type=parse_size, default=[(3, 3), (4, 4)],
                        help="grid sizes, e.g. 3x3 4x4 (default: 3x3 4x4)")
    parser.add_argument("-n", "--count", type=int, default=5, help="puzzles per level for every size (default: 5)")
    parser.add_argument("-s", "--seed", type=int, help="first seed (default: random)")
    args = parser.parse_args()

    puzzles = export(args.sizes, args.count, first_seed=args.seed)
    print(f"Saved {len(puzzles)} puzzles to web/puzzles.js")


if __name__ == "__main__":
    main()
