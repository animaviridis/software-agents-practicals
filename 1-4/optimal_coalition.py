"""Identify the optimal coalition structure, that is, identify what
agents should be allocated to which coalition to maximise the sum of utility. The simplest
way to compute this involves computing the sum of utilities for every possible combination
of coalitions, and picking the highest one.

Implement a simple algorithm to compute the optimal coalition structure.
Your algorithm should simply generate all possible partitions and compute their value, finally
returning the maximal one. Keep track of the time taken to run for 1,2, . . . agents. At
what point does the algorithm start to take too long to run? """


import numpy as np


def generate_utilities(n):
    return dict(zip(range(1, n + 1), np.random.randint(1, 100, n)))


def combinations(nums: list, n_left):
    if n_left < 2:
        return [[num] for num in nums]

    c = []
    for i in range(len(nums)-n_left + 1):
        head = [nums[i]]
        tail = nums[i+1:]
        print(head, tail)
        c += [head + ni for ni in combinations(tail, n_left-1)]

    return c


def split_combinations(nums: list, n_left):
    if n_left < 2:
        r = []
        for i in range(len(nums)):
            r.append((nums[i], nums[:i]+nums[i+1:]))
        return r

    c = []
    for i in range(len(nums)-n_left + 1):
        head = [nums[i]]
        tail = nums[i+1:]
        print(head, tail)

        for ni in combinations(tail, n_left-1):
            c.append((head + ni[0], ni[1]))

    return c


if __name__ == '__main__':
    N = 2  # number of agents
    utilities = generate_utilities(N)
    print(f"{N} agents with utilities: {utilities}")

