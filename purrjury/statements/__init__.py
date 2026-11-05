from purrjury.statements.count_liars import CountLiars
from purrjury.statements.pair import PairStatement
from purrjury.statements.only import Only
from purrjury.statements.all_same import AllSame
from purrjury.statements.if_then import IfThen
from purrjury.statements.hearsay import Hearsay
from purrjury.statements.compare import Compare
from purrjury.statements.odd import OddLiars
from purrjury.statements.next_to import NextToEachOther
from purrjury.statements.individualist import Individualist

# Every statement type the generator can pick from. Add new types here.
ALL_STATEMENTS = [CountLiars, PairStatement, Only, AllSame, IfThen, Compare, OddLiars, NextToEachOther, Individualist]

# Hearsay isn't in the list on purpose: it needs a hidden cat, so the generator adds it separately
