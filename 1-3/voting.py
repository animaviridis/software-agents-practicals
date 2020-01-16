import pandas as pd
import argparse


def import_data(fname: str, sheet=0):
    print(f"importing data from file '{fname}'")
    data = pd.read_excel(fname, index_col=0, sheet_name=sheet)

    return data


def sort_scores(func):
    def wrapper(*args, **kwargs):
        return func(*args, *kwargs).sort_values(ascending=False)
    return wrapper


@sort_scores
def vote_plurality(data: pd.DataFrame):
    m = data.max().max()
    return (d == m).sum()


@sort_scores
def vote_borda(data: pd.DataFrame):
    return data.sum()


def is_equal_or_null(d1, d2):
    return (d1.eq(d2) + d1.isnull() + d2.isnull()).all().all()


def vote_runoff(data: pd.DataFrame, n_rounds=2, verbose=False):
    if n_rounds < 1:
        raise ValueError("Number of rounds must be a positive integer")

    all_scores = vote_plurality(data)
    best_scores = all_scores[:n_rounds]

    if verbose:
        print(f"---Rounds left: {n_rounds}, scores:\n{all_scores}")

    if n_rounds < 2:
        return best_scores
    else:
        return vote_runoff(data[best_scores.index], n_rounds=n_rounds-1, verbose=verbose)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-fname', type=str, default=r"..\1-3\countries.xlsx")
    parser.add_argument('-sheet', default=0)

    parsed_args = parser.parse_args()
    d = import_data(parsed_args.fname, parsed_args.sheet)
    print(f"\nPlurality vote:\n{vote_plurality(d)}")
    print(f"\nBorda count vote:\n{vote_borda(d)}")
    print(f"\nRunoff vote (2 rounds):\n{vote_runoff(d)}")
    print(f"\nRunoff vote (3 rounds):\n{vote_runoff(d, 3)}")

    print(f"\n{20*'-'}\nComparing matrices")
    dd = d[:2]
    dd2 = dd.fillna(0)
    print(dd, '\n', dd2, '\n', is_equal_or_null(dd, dd2))

