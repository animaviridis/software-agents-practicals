class Atom:
    def __init__(self, neg, literal):
        self.negated = neg
        self.literal = literal

    def neg(self):
        return Atom(not self.negated, self.literal)

    def contrary(self, atom):
        return self.neg() == atom

    def __hash__(self):
        return hash((self.negated, self.literal))

    def __eq__(self, other):
        return isinstance(other, type(self)) and self.negated == other.negated and self.literal == other.literal

    def __repr__(self):
        if self.negated:
            return "!" + str(self.literal)
        else:
            return self.literal
