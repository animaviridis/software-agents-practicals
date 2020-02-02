from argparse import ArgumentParser


def parse_cmd_args(add_principles=False, add_extension=False):
    parser = ArgumentParser()
    parser.add_argument('fname', type=str, help="Data file name")
    parser.add_argument('--verbose', action='store_true', dest='verbose')

    if add_principles:
        parser.add_argument('principle', type=str, choices=['wd', 'we', 'ld', 'le'],
                            help='preference principles: weakest/last and democratic/elitist')
        parser.add_argument('restr', type=str, choices=['true', 'false'])

    if add_extension:
        parser.add_argument('extension', type=str, choices=["grounded", "preferred", "stable"],
                            help="Extension to be computed")

    parsed_args = parser.parse_args()
    if add_principles:
        parsed_args.weakest = parsed_args.principle[0] == 'w'
        parsed_args.elitist = parsed_args.principle[1] == 'e'
        parsed_args.restr = parsed_args.restr == 'true'

    return parsed_args


class NameDict(dict):
    def __init__(self, items):
        super(NameDict, self).__init__({i.name: i for i in items})

    def __repr__(self):
        return str(set(self.values()))

    def __iter__(self):
        yield from self.values()
