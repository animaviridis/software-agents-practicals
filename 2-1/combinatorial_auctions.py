"""Create a brute-force winner determination mechanism for XOR-bids based combinatorial
auctions. As input, your mechanism should take XOR-bids from a set of agents, and should
then output an allocation as well as the social welfare obtained."""


def parse_bid(bid):
    bid_dict = dict()
    sub_bids = bid.lower().split(' xor ')

    if 'xor' in bid.lower() and len(sub_bids) < 2:
        print("Invalid bid format: sub-bids should be separated with ' xor ' (with spaces around)")
        return

    for sub_bid in sub_bids:
        if ':' not in sub_bid:
            print("Invalid bid format: sub-bids should have the format: <good1, good2, ...> : <value>")
            return

        goods, value = sub_bid.replace(' ', '').split(':')

        try:
            value_num = float(value)
        except ValueError:
            print(f"Invalid sub-bid value: {value}")
            return

        if not goods and value_num > 0:
            print(f"An empty sub-bid should be associated with the value of 0 (got {value_num})")
            return

        bid_dict[tuple(goods.split(','))] = value_num

    return bid_dict


def record_bid():
    b = None
    while b is None:
        b = parse_bid(input("Enter a (XOR) bid: "))

    return b


if __name__ == '__main__':

    print(f"Your XOR bid: {record_bid()}")

