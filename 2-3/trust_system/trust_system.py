import random
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt

from class_2_3.trust_system.agent import DummyAgent
from class_2_3.trust_system.environment import Environment


Agent = DummyAgent
NUM_AGENTS = 10  # Number of agents

random.seed(0)  # set the random seed
agents = []
for i in range(0, NUM_AGENTS):
    agents.append(Agent(random.random()))

# create a complete graph,
# see https://networkx.github.io/documentation/stable/reference/generators.html for other generators
graph = nx.complete_graph(NUM_AGENTS)
env = Environment(graph)
env.add_agents(agents)

# random.seed(time.time()) # uncomment if you want different experiments on same graph
n_rounds = 100
all_scores = np.zeros((n_rounds, 2))
for i in range(0, n_rounds):  # run for 100 rounds
    score = [0, 0]
    for a in env.nodes:
        s = a.delegate()
        if s:
            score[0] += 1
        else:
            score[1] += 1
    all_scores[i] = score

fig, ax = plt.subplots()
ax.plot(all_scores[:, 0], all_scores[:, 1], 'o', alpha=0.05, markersize=15)
plt.show()
