import pandas as pd
import argparse
import itertools as it
import numpy as np


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
    return (data == m).sum()


@sort_scores
def vote_borda(data: pd.DataFrame):
    return data.sum()


def unfold_tuple(t):
    return tuple(el for subt in t for el in subt)


def generate_votes(data: pd.DataFrame, start=1):
    all_options = set(range(start, start+data.shape[1]))
    missing = [all_options.difference(set(i)) for i in data.values]
    missing_generator = it.product(*tuple(tuple(it.permutations(i)) for i in missing))

    missing_loc = np.where(data.isna())
    template_arr = np.array(data)

    def gen():
        for fill in missing_generator:
            template_arr[missing_loc] = unfold_tuple(fill)
            yield pd.DataFrame(template_arr, index=d.index, columns=d.columns)

    return gen()


def vote_runoff(data: pd.DataFrame, n_rounds=2, verbose=False):
    # TODO: correct
    def rec(names=None, n_rounds_=2):
        names = names if names is not None else data.columns
        if n_rounds_ < 1:
            raise ValueError("Number of rounds must be a positive integer")

        all_scores = vote_plurality(data[names])
        best_scores = all_scores[:n_rounds_]

        if verbose:
            print(f"---Rounds left: {n_rounds_}, scores:\n{all_scores}")

        if n_rounds_ < 2:
            return best_scores
        else:
            return rec(best_scores.index, n_rounds_=n_rounds_-1)

    return rec(None, n_rounds)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-fname', type=str, default=r"..\1-3\countries.xlsx")
    parser.add_argument('-sheet', default=0)

    parsed_args = parser.parse_args()
    d = import_data(parsed_args.fname, parsed_args.sheet)
    print(f"\nPlurality vote:\n{vote_plurality(d)}")
    print(f"\nBorda count vote:\n{vote_borda(d)}")
    print(f"\nRunoff vote (2 rounds):\n{vote_runoff(d)}")
    print(f"\nRunoff vote (3 rounds):\n{vote_runoff(d, 3, True)}")

    for vote in generate_votes(d):
        if vote_plurality(vote).index[0] == 'Italy':
            print("\n\nItaly winning in plurality: \n")
            print(vote)
            break

