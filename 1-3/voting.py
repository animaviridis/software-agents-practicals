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


def vote_runoff(data: pd.DataFrame):
    first_round_scores = vote_plurality(data)
    second_round_data = data[first_round_scores.index[:2]]
    second_round_scores = vote_plurality(second_round_data)
    return second_round_scores[0:1]  # the winner as a pd.Series


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-fname', type=str, default=r"..\1-3\countries.xlsx")
    parser.add_argument('-sheet', default=1)

    parsed_args = parser.parse_args()
    d = import_data(parsed_args.fname, parsed_args.sheet)
    print(f"\nPlurality vote:\n{vote_plurality(d)}")
    print(f"\nBorda count vote:\n{vote_borda(d)}")
    print(f"\nRunoff vote (2 rounds): {vote_runoff(d)}")

