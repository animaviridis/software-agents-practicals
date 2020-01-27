import numpy as np
import pandas as pd


def normalise_trust(local_trust):
    local_trust_positive = local_trust.where(local_trust > 0, 0)

    local_trust_norm = local_trust_positive.div(local_trust_positive.sum(axis=1), axis=0)
    return local_trust_norm


if __name__ == '__main__':
    n_agents = 3
    agents = list(range(n_agents))

    trust = pd.DataFrame(np.random.randint(-3, 10, size=(n_agents, n_agents)),
                         columns=[f'trustee A{i}' for i in agents],
                         index=[f'trustor A{i}' for i in agents])

    print(trust)
    trust_norm = normalise_trust(trust)
    print(trust_norm)
