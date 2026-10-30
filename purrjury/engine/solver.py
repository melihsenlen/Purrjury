"""A human-style solver: finds cats one step at a time, the way a player would.

A step uses 1 clue (easy) or 2 clues together (harder) plus the cats already known.
If no step works anymore before every cat is found, the puzzle isn't fun to solve.
"""
import itertools

from purrjury.board.grid import get_cat


# groups of clues about more unknown cats than this are skipped, nobody can juggle that many
MAX_UNKNOWN = 12

# Difficulty levels, easiest first
LEVELS = ["easy", "medium", "hard", "tricky"]

# Grids with this many cats or more are one level harder: there are more clues to scan for each move
BIG_GRID = 16


def involved(statement):
    """All cats a clue is about: its speaker plus the cats it mentions."""
    return  set(statement.mentions()) | {statement.speaker}


def forced_cats(statements, known, grid):
    """Which unknown cats are forced by these clues, given the cats we already know.

    statements: a list of 1 or 2 statements that are used together
    known:      dict {cat index: True if liar, False if honest} of the cats found so far
    Returns a dict {cat index: True/False} of newly forced cats (can be empty).
    """
    n_cats = len(grid) * len(grid[0])

    # the cats these clues are about that we don't know yet, in a fixed order
    unknown = sorted(set().union(*(involved(s) for s in statements)) - set(known))
    if not unknown or len(unknown) > MAX_UNKNOWN:
        return {}   # nothing to find, or too many cats for a human to juggle at once

    # for every unknown cat, the values it had in the combinations that fit
    seen = {cat: set() for cat in unknown}

    # try every combination of the unknown cats being honest (False) or a liar (True)
    for combo in itertools.product([False, True], repeat=len(unknown)):
        world = [False] * n_cats          # cats the clues don't look at can be anything
        for cat, value in known.items():
            world[cat] = value
        for cat, value in zip(unknown, combo):
            world[cat] = value

        # keep the combination only if every clue fits
        if all(s.fits(world, grid) for s in statements):
            for cat, value in zip(unknown, combo):
                seen[cat].add(value)

    # a cat that only ever had one value is forced
    # (if no combination fit at all, every set is empty and nothing is forced)
    return {cat: next(iter(values)) for cat, values in seen.items() if len(values) == 1}


def solve(grid, known=None):
    """Solve the puzzle step by step like a player.

    known: optional dict {cat index: True if liar} of cats the player is given from the start.

    Returns a list of steps, each one like (level, speakers, found, options):
        level:    1 or 2, how many clues the step needed
        speakers: indexes of the cats whose clues were used
        found:    dict {cat index: True/False} of the cats found in this step
        options:  how many clues (or pairs of clues) at this level would have found a cat here.
                  1 means the player had to find the one move that works, more means it was easier to spot
    Returns None if it gets stuck before every cat is found.
    """
    n_cats = len(grid) * len(grid[0])
    known = dict(known or {})   # a copy, so the caller's dict isn't changed
    steps = []

    # hidden cats only meow, so their own statements can't be used (same as in the checker)
    clues = [get_cat(grid, i).statement for i in range(n_cats)
             if get_cat(grid, i).statement is not None and not get_cat(grid, i).hidden]

    # keep finding cats until every cat is known
    while len(known) < n_cats:
        step = None

        # easiest first: one clue on its own, then two clues together
        for level in (1, 2):
            # every clue (or pair) at this level that finds a new cat, so we know how many options there were
            usable = []
            for group in itertools.combinations(clues, level):
                found = forced_cats(list(group), known, grid)
                if found:
                    usable.append((group, found))

            if usable:
                # only the first one is used as the step, the others are just counted
                group, found = usable[0]
                speakers = [s.speaker for s in group]
                step = (level, speakers, found, len(usable))
                break

        if step is None:
            return None   # stuck: no single clue or pair of clues finds a new cat

        known.update(step[2])
        steps.append(step)

    return steps


def levels_for(rows, cols):
    """The 3 levels a grid of this size can get: easy to hard, or medium to tricky on a big grid."""
    bump = 1 if rows * cols >= BIG_GRID else 0
    return LEVELS[bump:bump + 3]
