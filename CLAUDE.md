# Purrjury

Daily logic puzzle: a grid of cats, honest cats always tell the truth, liars always lie, each cat has one clue. Find the liars.
Python engine in `purrjury/`, plain HTML/CSS/JS site in `web/` (GitHub Pages: yusufsocal.github.io/Purrjury/web).
Design by Brojum (Yusuf), most code written by Claude.

## How to work with me
- Short, direct answers. No em dashes. Call me Brom or Brojum now and then.
- Talk before big changes, walk me through what changed afterwards. I want to understand the code.
- Give me commit commands to copy: short conventional commits (`feat(web): ...`, `fix(engine): ...`), split by topic.
  Put all the lines (add, commit, push) together in one block at the end of the message. Don't commit yourself unless I ask.
- My terminal is PowerShell: give commands in PowerShell syntax.
- Files use CRLF line endings. Keep CRLF when editing. Use `git diff --ignore-cr-at-eol` to see real changes.
- For UI changes with several options, show mockups first.
- Don't make me wait on long background jobs. Tell me as soon as the important part is done.

## Commands
- Tests: `python -m pytest -q` (keep them green)
- Export puzzles to the site: `python export.py` (writes `web/puzzles.js`)
- The page footer says when the puzzles were made. If it's old, the browser cached `puzzles.js` (Ctrl+F5).

## Design rules (settled, don't re-argue)
- All clues are visible from the start. Every puzzle is solvable by logic alone and has a unique answer.
- Fun = chaining: a solved cat's clue reveals the next. No domino reveals where one clue gives away many cats.
- Neighbors = up, down, left, right only.
- One plain wording per clue type, only the words "honest" and "liar". No negative wordings (a test enforces it).
- A clue's logic may only use what its text says. No hidden assumptions.
- Variety matters: a puzzle shouldn't read like the same sentence over and over.
- Cat sounds are picked from a clue's words only, never from the answer.
- Puzzles are pre-generated and saved, so code changes never alter old puzzles.
- Rules alone can't judge difficulty; playtesting decides.

## Code map
- `purrjury/board/`: grid, cats, colors, areas
- `purrjury/statements/`: one file per clue type; `purrjury/texts.py` has all wordings
- `purrjury/engine/`: solver (solves like a person), path generator (builds puzzles along a solving path), old random generator
- `export.py`: difficulty settings per level, makes and saves the puzzles for the site
- `web/`: the site (`game.js`, `style.css`, `puzzles.js`)
