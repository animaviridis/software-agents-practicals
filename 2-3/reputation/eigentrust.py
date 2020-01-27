import pandas as pd


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


if __name__ == '__main__':
    f = r'2-3/reputation/local_trust.xlsx'
    print(f"Importing from {f}")
    trust = pd.read_excel(f, index_col=0)
    print(trust)

    trust_norm = normalise_trust(trust)
    print(trust_norm)

    trust_agg = trust_norm.iloc[0]
    print(f"\nInitial trust:\n{trust_agg}")

    LIM = 1e-3
    d = 1
    i = 1

    agg = aggregate(trust_norm)

    while d >= LIM:
        trust_agg, d = agg(trust_agg)
        i += 1

    print(f"\nTrust aggregation - {i} rounds,  diff={d:.2E}:\n{trust_agg}")
