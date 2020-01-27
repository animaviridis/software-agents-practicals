import numpy as np
import pandas as pd


def normalise_trust(local_trust):
    local_trust_positive = local_trust.where(local_trust > 0, 0)

    local_trust_norm = local_trust_positive.div(local_trust_positive.sum(axis=1), axis=0)
    return local_trust_norm


def mul(trust_matrix, trust_vector):
    trust_vector_reind = pd.Series(trust_vector.values, index=trust_matrix.index, name=trust_vector.name)

    return trust_matrix.T.dot(trust_vector_reind)


if __name__ == '__main__':
    n_agents = 3
    agents = list(range(n_agents))

    trust = pd.DataFrame(np.random.randint(-3, 10, size=(n_agents, n_agents)),
                         columns=[f'trustee A{i}' for i in agents],
                         index=[f'trustor A{i}' for i in agents])

    print(trust)
    trust_norm = normalise_trust(trust)
    print(trust_norm)

    trust_agg = trust_norm.iloc[0]
    print(f"\nInitial trust:\n{trust_agg}")

    trust_agg = mul(trust_norm, trust_norm.iloc[0])
    print(f"\nFirst-order trust aggregation:\n{trust_agg}")
