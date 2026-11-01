"""Sentences for statements. Placeholders:
    {name}  a single cat's name
    {area}  the area text, e.g. "my neighbors", "the orange cats", "the cats in the grid"
    {n}     the number of liars
    {h}     the number of honest cats (size of the area minus n)
    {a} {b}            the two cats in a pair statement
    {opposite} {then}  the types in an IfThen statement
    {quote}            what a hidden cat supposedly said
One plain wording per kind of clue, so the same logic always looks the same. Only the words
honest and liar, no synonyms. The cat talk is a sound the generator sometimes adds before or
after a clue (CAT_SOUNDS), plus a few puns on the simplest clue.
No negative wordings (not, none, can't, at most, ...): when a liar says one, the player
would have to un-negate twice.
"""

INDIVIDUALIST = [
    "I'm telling the truth!",
    "I'm righteous!",
    "I'm honest.",
]

# --- Cat sounds ---
# The generator puts one before or after some clues (see add_cat_sounds in generator.py).
# The mood comes from what the clue says ("X is a liar" is angry), never from whether the speaker
# is really honest, so a sound never gives anything away.


CAT_SOUNDS = {
    "happy": ["Purr.", "Prrrt!", "Mrrp!"],
    "angry": ["Hiss!", "Grrr.", "Pfft!"],
    "neutral": ["Meow.", "Mrow.", "Mew."],
}


# --- One specific cat (area of size 1) ---

LIAR_TEXTS = [
    "{name} is a liar.",
]

HONEST_TEXTS = [
    "{name} is honest.",
    "{name} is pawsitively honest.",
    "{name} is honest, fur real.",
    "{name} is honest. That's a purr-fact.",
]


# --- Counting in an area (area of size 2 or more) ---

# exactly 0
NONE_TEXTS = [
    "All of {area} are honest.",
]

# exactly all of them
ALL_TEXTS = [
    "All of {area} are liars.",
]

# exactly 1 (but not all)
EXACTLY_ONE_TEXTS = [
    "Exactly one of {area} is a liar.",
]

# exactly n, with n of 2 or more (but not all)
EXACTLY_N_TEXTS = [
    "Exactly {n} of {area} are liars.",
]

# at least 1
AT_LEAST_ONE_TEXTS = [
    "At least one of {area} is a liar.",
    "I smell a rat. At least one of {area} is a liar.",
]

# at least n, with n of 2 or more (but not all)
AT_LEAST_N_TEXTS = [
    "At least {n} of {area} are liars.",
]


# --- Two cats (PairStatement) ---
# {a} and {b} are cat names. The _ME_ lists are used when the speaker is a: only {b}, the speaker is "I"/"me".

PAIR_SAME_TEXTS = [
    "{a} and {b} are both honest, or both liars.",
]

PAIR_SAME_ME_TEXTS = [
    "{b} and I are both honest, or both liars.",
]

PAIR_DIFFERENT_TEXTS = [
    "{a} and {b} are opposites: one is honest, the other is a liar.",
]

PAIR_DIFFERENT_ME_TEXTS = [
    "{b} and I are opposites: one is honest, the other is a liar.",
]

PAIR_AT_LEAST_ONE_LIAR_TEXTS = [
    "At least one of {a} and {b} is a liar.",
]

PAIR_AT_LEAST_ONE_LIAR_ME_TEXTS = [
    "At least one of {b} and me is a liar.",
]

PAIR_AT_LEAST_ONE_HONEST_TEXTS = [
    "At least one of {a} and {b} is honest.",
]

PAIR_AT_LEAST_ONE_HONEST_ME_TEXTS = [
    "At least one of {b} and me is honest.",
]

PAIR_BOTH_LIARS_TEXTS = [
    "{a} and {b} are both liars.",
]

PAIR_BOTH_LIARS_ME_TEXTS = [
    "{b} and I are both liars.",
]

PAIR_BOTH_HONEST_TEXTS = [
    "{a} and {b} are both honest.",
]

PAIR_BOTH_HONEST_ME_TEXTS = [
    "{b} and I are both honest.",
]

# "If a is honest, then b is honest" is written as "a is a liar, or b is honest (at least one is true)",
# same thing, but much easier to work with when the speaker turns out to be a liar
PAIR_IF_A_HONEST_THEN_B_TEXTS = [
    "At least one of these is true: {a} is a liar, or {b} is honest.",
]

PAIR_IF_A_HONEST_THEN_B_ME_TEXTS = [
    "At least one of these is true: I'm a liar, or {b} is honest.",
]

PAIR_A_HONEST_B_LIAR_TEXTS = [
    "{a} is honest, but {b} is a liar.",
]

PAIR_A_HONEST_B_LIAR_ME_TEXTS = [
    "I'm honest, but {b} is a liar.",
]


# --- The only one in an area (Only) ---
# {name} is the cat, {area} is the area text. The _ME_ lists are used when the speaker is that cat.

ONLY_ME_LIAR_TEXTS = [
    "I'm the only liar among {area}.",
]

ONLY_ME_HONEST_TEXTS = [
    "I'm the only honest cat among {area}.",
]

ONLY_LIAR_TEXTS = [
    "{name} is the only liar among {area}.",
]

ONLY_HONEST_TEXTS = [
    "{name} is the only honest cat among {area}.",
]


# --- Whole area the same type or not (AllSame) ---
# {area} is the area text.

ALL_SAME_TEXTS = [
    "All of {area} are the same: all honest, or all liars.",
]

MIXED_TEXTS = [
    "Among {area}, at least one is honest and at least one is a liar.",
]


# --- If a cat is something, a whole area is something (IfThen) ---
# "If A, then B" is written as "At least one of these is true: not A, or B". Same thing, easier to read.
# {name} is the cat, {opposite} is the opposite of the "if" part ("honest" or "a liar"),
# {area} is the area text, {then} is "honest" or "liars".

IF_THEN_TEXTS = [
    "At least one of these is true: {name} is {opposite}, or all of {area} are {then}.",
]


# --- Two areas compared (Compare) ---
# {a} and {b} are area texts with their own small word in front: "in row 1", "among my neighbors".

COMPARE_MORE_LIARS_TEXTS = [
    "There are more liars {a} than {b}.",
]

COMPARE_MORE_HONEST_TEXTS = [
    "There are more honest cats {a} than {b}.",
]

COMPARE_SAME_TEXTS = [
    "There are as many liars {a} as {b}.",
]


# --- An odd number of liars in an area (OddLiars) ---
# Only "odd": an "even" clue would make players wonder whether 0 counts.

ODD_TEXTS = [
    "An odd number of {area} are liars.",
]


# --- Liars (or honest cats) connected (NextToEachOther) ---
# Connected: one group where you can walk from any of them to any other, only stepping on that type.
# The "2 or more" is part of the claim and the text says so: a liar saying it can mean there are only 0 or 1.
# {line} is "Row 2", "My row", "Column 3" or "My column".

NEXT_TO_LIARS_TEXTS = [
    "{line} has 2 or more liars, all connected.",
]

NEXT_TO_HONEST_TEXTS = [
    "{line} has 2 or more honest cats, all connected.",
]

# the whole grid
EVERYONE_NEXT_TO_LIARS_TEXTS = [
    "There are 2 or more liars, all connected.",
]

EVERYONE_NEXT_TO_HONEST_TEXTS = [
    "There are 2 or more honest cats, all connected.",
]


# --- Areas that cover every cat ---
# Only counts use the whole grid. Every puzzle has at least one liar and at least one honest cat,
# so "every cat is honest", "at least one liar in total" or "all the cats are the same" are always
# settled and would only give the speaker away.
# The normal texts would say "exactly 5 of the cats in the grid", so these get their own wording.

EVERYONE_EXACTLY_ONE_TEXTS = [
    "There's exactly one liar in total.",
]

EVERYONE_EXACTLY_N_TEXTS = [
    "There are exactly {n} liars in total.",
]

# at least n, with n of 2 or more
EVERYONE_AT_LEAST_N_TEXTS = [
    "There are at least {n} liars in total.",
]


# --- Hidden cats and what other cats heard them say (Hearsay) ---
# A hidden cat only meows, its real statement is only known through another cat.
# {name} is the hidden cat, {quote} is the statement it supposedly said, in its own words.

GIBBERISH_TEXTS = [
    "Mrrrow mrrp mew.",
    "Mrrp? Mew mew mrrrow!",
    "*incomprehensible meowing*",
    "Nyaa... mrrp. Mew.",
    "*chirps at a bird outside*",
]

HEARSAY_TEXTS = [
    '{name} said: "{quote}"',
    '{name} told me: "{quote}"',
]
