class Rule:
    def __init__(self, name, premises, conc, strict):
        self.name = name
        self.premises = premises
        self.conclusions = conc
        self.strict = strict

    def __repr__(self):
        s = "=>"
        if self.strict:
            s = "->"
        p = ""
        for pr in self.premises:
            p += ", " + str(pr)
        p = p[1:]
        return "" + self.name + ":" + p + " " + s + " " + str(self.conclusions)

    def __hash__(self):
        s = 0
        if len(self.premises) > 0:
            for p in self.premises:
                s += hash(p)
        return hash((s, self.name, self.conclusions, self.strict))

    def __eq__(self, other):
        if type(self) != type(other):
            return False
        if self.premises - other.premises != set() or other.premises - self.premises != set():
            return False
        return self.name == other.name and self.conclusions == other.conc and self.strict == other.strict
