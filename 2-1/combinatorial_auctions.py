"""Create a brute-force winner determination mechanism for XOR-bids based combinatorial
auctions. As input, your mechanism should take XOR-bids from a set of agents, and should
then output an allocation as well as the social welfare obtained.

Example:
3 agents with bids:
- a: 3 xor a, b: 100 xor c: 4
- a, b: 2 xor d: 20
- c: 20 xor a, d: 21

-> Result:
Best allocation: {0: {'b', 'a'}, 1: {'d'}, 2: {'c'}} (social welfare: 140.0)
"""


import re
import itertools as it
import numpy as np
from collections.abc import Iterable

from misc import misc

BID_PATTERN = r'(\w*\s*,\s*)*\w+\s*:\s*\d+'


class BidDict(dict):
    def _get_valuation(self, goods):
        if not isinstance(goods, Iterable):
            goods = (goods,)
        goods_set = set(goods)

        max_val = 0
        for key, value in self.items():
            if set(key).issubset(goods_set):
                if value > max_val:
                    max_val = value

        return max_val

    def __getitem__(self, item):
        return self._get_valuation(item)


def parse_bid(bid):
    bid_dict = BidDict()
    sub_bids = bid.lower().split(' xor ')

    if 'xor' in bid.lower() and len(sub_bids) < 2:
        print("Invalid entry: sub-bids should be separated with ' xor ' (with spaces around)")
        return

    for sub_bid in sub_bids:
        if re.fullmatch(BID_PATTERN, sub_bid) is None:
            print(f"Invalid entry: sub-bids should have the format: <good1, good2, ...> : <value> (got '{sub_bid}')")
            return

        goods, value = sub_bid.replace(' ', '').split(':')
        value_num = float(value)

        if not goods and value_num > 0:
            print(f"Invalid entry: an empty sub-bid should be associated with the value of 0 (got {value_num})")
            return

        bid_dict[tuple(goods.split(','))] = value_num

    return bid_dict


def record_bid(agent=None):
    b = None
    while b is None:
        b = parse_bid(input(f"Enter a (XOR) bid for agent{' ' + agent if agent else ''}: "))

    return b


def collect_data():
    n = misc.validate("Enter the number of agents: ", int)

    agents = []
    for i in range(n):
        agents.append(record_bid(str(i)))

    return agents


def extract_items(agents):
    all_items = set()
    for agent in agents:
        for key in agent.keys():
            for item in key:
                all_items.add(item)

    return sorted(all_items)


def allocate(agents):
    all_items = extract_items(agents)
    print(f"\nItems to be distributed: {all_items}")
    all_items = np.array(all_items)

    rn = range(len(agents))
    best_alloc = ()
    best_social_welfare = 0

    for alloc_c in it.combinations_with_replacement(rn, len(all_items)):
        for alloc in set(it.permutations(alloc_c)):
            alloc_arr = np.array(alloc)
            print(f"\nAllocation: {dict(zip(all_items, alloc_arr))}")

            social_welfare = 0
            alloc_by_agent = dict()

            for i, agent in enumerate(agents):
                items_i = all_items[np.where(alloc_arr == i)]
                alloc_by_agent[i] = set(items_i)
                value_i = agent[items_i]
                print(f"Agent {i}: {items_i} = {value_i}")
                social_welfare += value_i
            print(f"Social welfare: {social_welfare}")

            if social_welfare > best_social_welfare:
                best_social_welfare = social_welfare
                best_alloc = alloc_by_agent

    return best_alloc, best_social_welfare


def main():
    all_agents = collect_data()
    print(all_agents)

    allocation, score = allocate(all_agents)
    print(f"\n{20 * '-'}\nBest allocation: {allocation} (social welfare: {score})\n")


if __name__ == '__main__':
    main()
