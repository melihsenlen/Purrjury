import random

from purrjury.statements.base import Statement
from purrjury import texts


class Individualist(Statement):
    """
    A cat that only speaks for itself, claiming to be right.
    """

    def evaluate(self, world, grid):
        return not world[self.speaker] # Makes no sense btw

    def mentions(self):
        return [] # lol

    def key(self):
        return ("individualist",)

    def mood(self):
        return "happy" # :) it says something nice about itself

    def set_text(self, grid):
        self.text = random.choice(texts.INDIVIDUALIST_TEXTS)

    @classmethod
    def random(cls, speaker, grid, world):
        statement = cls(speaker)
        statement.set_text(grid)
        return statement