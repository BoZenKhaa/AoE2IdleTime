import os

from mgz import header, fast
from mgz.fast import Operation

NEEDED_RECODING_DATA = [Operation.CHAT, Operation.ACTION, Operation.SYNC]


def load_replay(pathfile):
    game_data = []
    with open(pathfile, 'rb') as data:
        eof = os.fstat(data.fileno()).st_size
        header.parse_stream(data)
        fast.meta(data)
        while data.tell() < eof:
            op_type, val = fast.operation(data)
            if op_type in NEEDED_RECODING_DATA:
                game_data.append((op_type, val))

    return game_data