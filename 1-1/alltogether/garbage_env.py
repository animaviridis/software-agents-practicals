#!/usr/bin/env python

from agentspeak import runtime, stdlib
import os


here = os.path.dirname(__file__)

env = runtime.Environment()

with open(os.path.join(here, "garbage_sensor.asl")) as source:
    agents = env.build_agents(source, 1, stdlib.actions)

with open(os.path.join(here, "garbage_collector.asl")) as source:
    agents.append(env.build_agent(source, stdlib.actions))


if __name__ == "__main__":
    env.run()
