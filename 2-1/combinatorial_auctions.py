"""Create a brute-force winner determination mechanism for XOR-bids based combinatorial
auctions. As input, your mechanism should take XOR-bids from a set of agents, and should
then output an allocation as well as the social welfare obtained."""


import re


BID_PATTERN = r'(\w*\s*,\s*)*\w+\s*:\s*\d+'


def parse_bid(bid):
    bid_dict = dict()
    sub_bids = bid.lower().split(' xor ')

    if 'xor' in bid.lower() and len(sub_bids) < 2:
        print("Invalid entry: sub-bids should be separated with ' xor ' (with spaces around)")
        return

    for sub_bid in sub_bids:
        if re.match(BID_PATTERN, sub_bid) is None:
            print(f"Invalid entry: sub-bids should have the format: <good1, good2, ...> : <value> (got '{sub_bid}')")
            return

        goods, value = sub_bid.replace(' ', '').split(':')
        value_num = float(value)

        if not goods and value_num > 0:
            print(f"Invalid entry: an empty sub-bid should be associated with the value of 0 (got {value_num})")
            return

        bid_dict[tuple(goods.split(','))] = value_num

    return bid_dict


def record_bid():
    b = None
    while b is None:
        b = parse_bid(input("Enter a (XOR) bid: "))

    return b


def get_valuation(goods, val_dict):
    goods_set = set(goods)

    max_val = 0
    for key, value in val_dict.items():
        if set(key).issubset(goods_set):
            if value > max_val:
                max_val = value

    return max_val


if __name__ == '__main__':

    br = record_bid()
    print(f"Your XOR bid: {br}")

