# Playtest notes

What players said about the puzzles, so changes are based on feedback and not on guesses.
Nothing gets changed from one person's notes alone: an idea moves to "Try next" once others say the same.

## Feedback set (05 Nov 2026)

The 6 puzzles in `web/feedback_puzzles.js`, played at `index.html?set=feedback`.
Made with `python export.py 3x3 4x4 -n 1 -p web/feedback_puzzles.js`; the easy one was remade after the "shown cat goes first" change.

| Puzzle | Seed | Liars | Notes |
|---|---|---|---|
| 3x3 easy | 555108 | 5 of 9 | shown cat: Cricket (honest), "Row 3 has 2 or more liars, all connected." |
| 3x3 medium | 555109 | 3 of 9 | |
| 3x3 hard | 555110 | 7 of 9 | |
| 4x4 medium | 555111 | 9 of 16 | |
| 4x4 hard | 555112 | 8 of 16 | |
| 4x4 tricky | 555113 | 4 of 16 | |

## Brom (designer, knows how the generator thinks)

| Puzzle | Time | Hints | How it felt |
|---|---|---|---|
| 3x3 easy (old version) | 1:30 | 0 | Easy for me, but only because I know how the clues work. The shown cat's own clue was no use until the second half, while a new player would try it first. (Fixed: the shown cat's clue is now the first step.) |
| 3x3 medium | about 3:00 | 0 | Kinda whatever. |
| 3x3 hard | | 0 | VERY fun. Indigo (liar): "An odd number of Ember's neighbors are liars", and Indigo is one of Ember's neighbors, so the clue forces another cat either way. Having 7 liars instead of a third felt nice, probably makes it somewhat harder. |
| 4x4 medium | | | |
| 4x4 hard | | | |
| 4x4 tricky | | | |

Earlier (30 Oct 2026): Espresso's opener "There are more liars among Hazel's neighbors than in column 3" was "cool as hell". Espresso is one of Hazel's neighbors and the other one was shown honest, so if Espresso were honest there'd be 0 liars there, and 0 can't be "more": Espresso has to be a liar.

## Patterns so far

- **Clues that include their own speaker are fun.** "Ember's neighbors" when the speaker is one of them, "more liars among Hazel's neighbors" when the speaker is one of them. They make you think about the speaker and someone else at once, and they still reveal just 1 cat. (2 puzzles, 1 player)
- **More liars may be more fun and harder.** Every liar's clue has to be flipped in your head. Hard with 7 of 9 liars was very fun, medium with 3 of 9 was flat. (2 puzzles, 1 player)

## Ideas to try, once others agree

- Every puzzle gets at least 1 or 2 clues whose area includes the speaker.
- More liars on harder levels: hard and tricky mostly 50 to 75% liars, easy and medium closer to a third.

## Other players

(one section per player, same table as above)
