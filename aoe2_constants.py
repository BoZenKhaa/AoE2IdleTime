import os
from enum import Enum

from mgz import header, fast
from mgz.fast import Operation
from mgz.summary import Summary


class Ages(Enum):
    DARK = 0
    FEUDAL = 1
    CASTLE = 2
    IMPERIAL = 3


class EntityIDs(Enum):
    # Units
    VILLAGER = 83

    # Technologies
    LOOM = 22
    WHEELBARROW = 213
    HANDCART = -1000000000  # TODO: find actual id
    TOWNWATCH = 8
    TOWNPATROL = -10000000000  # TODO: find actual id
    FEUDAL_AGE = 101
    CASTLE_AGE = 102
    IMPERIAL_AGE = -100000000000  # TODO: find actual id


TRACKED_TECHNOLOGIES = [EntityIDs.LOOM, EntityIDs.WHEELBARROW, EntityIDs.HANDCART, EntityIDs.TOWNWATCH,
                        EntityIDs.TOWNPATROL, EntityIDs.FEUDAL_AGE, EntityIDs.CASTLE_AGE, EntityIDs.IMPERIAL_AGE]

BUILD_TIMES = {
    # Dark age
    EntityIDs.VILLAGER.value: 25000,
    EntityIDs.LOOM.value: 25000,
    EntityIDs.FEUDAL_AGE.value: 130000,

    # Feudal age
    EntityIDs.WHEELBARROW.value: 75000,
    EntityIDs.TOWNWATCH.value: 25000,
    EntityIDs.CASTLE_AGE.value: 160000,

    # Castle age
    EntityIDs.TOWNPATROL.value: 40000,
    EntityIDs.HANDCART.value: 55000,
    EntityIDs.IMPERIAL_AGE.value: 190000,
}







