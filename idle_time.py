import os
from mgz import header, fast
from mgz.summary import Summary


with open('data/AgeIIDE_Replay_257930563.aoe2record', 'rb') as data:
    # eof = os.fstat(data.fileno()).st_size
    # header.parse_stream(data)
    # fast.meta(data)
    # while data.tell() < eof:
    #     print(fast.operation(data))

    s = Summary(data)
    s.get_map()
    s.get_platform()
