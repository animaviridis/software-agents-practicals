"""Create a brute-force winner determination mechanism for XOR-bids based combinatorial
auctions. As input, your mechanism should take XOR-bids from a set of agents, and should
then output an allocation as well as the social welfare obtained."""


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


def allocate(agents):
    all_items = set()
    for agent in agents:
        for key in agent.keys():
            for item in key:
                all_items.add(item)

    print(f"\nItems to be distributed: {all_items}")

    all_items = np.array(sorted(all_items))

    rn = range(len(agents))
    best_alloc = ()
    best_social_welfare = 0

    for alloc in it.combinations_with_replacement(rn, len(all_items)):
        alloc_arr = np.array(alloc)
        alloc_dict = dict(zip(all_items, alloc_arr))
        print(f"\nAllocation: {alloc_dict}")
        social_welfare = 0

        for agent_n in rn:
            items_n = all_items[np.where(alloc_arr == agent_n)]
            value_n = agents[agent_n][items_n]
            print(f"Agent {agent_n}: {items_n} = {value_n}")
            social_welfare += value_n
        print(f"Social welfare: {social_welfare}")

        if social_welfare > best_social_welfare:
            best_social_welfare = social_welfare
            best_alloc = alloc_dict

    return best_alloc, best_social_welfare


def main():
    all_agents = collect_data()
    print(all_agents)

    allocation, score = allocate(all_agents)
    print(f"\n{20 * '-'}\nBest allocation: {allocation} (social welfare: {score})\n")


if __name__ == '__main__':
    main()
