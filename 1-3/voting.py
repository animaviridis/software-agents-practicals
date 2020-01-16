import pandas as pd
import argparse


def import_data(fname: str, sheet=0):
    print(f"importing data from file '{fname}'")
    data = pd.read_excel(fname, index_col=0, sheet_name=sheet)

    return data


def vote_plurality(data: pd.DataFrame):
    m = data.max().max()
    scores = (d == m).sum()
    return scores.sort_values(ascending=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-fname', type=str, default=r"..\1-3\countries.xlsx")
    parser.add_argument('-sheet', default=1)

    parsed_args = parser.parse_args()
    d = import_data(parsed_args.fname, parsed_args.sheet)
    print(f"Plurality vote:\n{vote_plurality(d)}")

