import networkx as nx


class Environment(nx.DiGraph):
    def add_agents(self, agents):
        m = {}
        i = 0
        for a in agents:
            m[i] = a
            i += 1
        nx.relabel_nodes(self, m, copy=False)

        for n in self.nodes:
            n.neighbours = set(nx.neighbors(self, n))

    def tick(self):
        score = [0, 0]
        for n in self.nodes:
            if n.delegate():
                score[0] += 1
            else:
                score[1] += 1
        return score
