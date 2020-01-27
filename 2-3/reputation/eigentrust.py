import pandas as pd
import numpy as np


def normalise_trust(local_trust):
    local_trust_positive = local_trust.where(local_trust > 0, 0)

    local_trust_norm = local_trust_positive.div(local_trust_positive.sum(axis=1), axis=0)
    return local_trust_norm


def mul(trust_matrix, trust_vector):
    trust_vector_reind = pd.Series(trust_vector.values, index=trust_matrix.index, name=trust_vector.name)

    return trust_matrix.T.dot(trust_vector_reind)


def diff(v1, v2):
    return (v1 - v2).abs().sum()


def aggregate(trust_matrix):
    def wrapper(trust_vector):
        trust_vector_agg = mul(trust_matrix, trust_vector)
        vd = diff(trust_vector, trust_vector_agg)
        return trust_vector_agg, vd
    return wrapper


def calculate_system_trust(trust_matrix_norm, lim=1e-6, init_vec='mean'):
    if init_vec == 'mean':
        system_trust = trust_norm.mean(axis=0)
    elif init_vec == 'random':
        system_trust = pd.Series(np.random.uniform(0.4, 0.6, size=3), index=trust_norm.columns)
    elif isinstance(init_vec, int):
        system_trust = trust_norm.iloc[init_vec]
    else:
        raise ValueError("init_vec should be 'mean', 'random', or an integer (column index)")

    print(f"\nInitial trust:\n{system_trust}")

    d = 1
    i = 0

    agg = aggregate(trust_matrix_norm)

    while d >= lim:
        system_trust, d = agg(system_trust)
        i += 1

    print(f"\nTrust aggregation - {i} rounds,  diff={d:.2E}")

    return system_trust


if __name__ == '__main__':
    f = r'2-3/reputation/local_trust.xlsx'
    print(f"Importing from {f}")
    trust = pd.read_excel(f, index_col=0)
    print(trust)

    trust_norm = normalise_trust(trust)
    print(f"\nNormalised trust: {trust_norm}")

    trust_agg = calculate_system_trust(trust_norm, init_vec='mean')
    print(f"System trust:\n{trust_agg}")
