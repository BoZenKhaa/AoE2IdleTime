# AoE2 Idle Town Center Time
This is a project to analyze the idle town center time of Age of Empires 2 players. The goal is to find out how much time players spend with their town center idle. 

Currently, only dark age idle time is analyzed. The results look ok, but it's not yet validated.

To try out, run the 'idle_time.py' script and set the constant `REPLAY` to a path pointing to a replay you want to analyze.

The notebook `dev.ipynb` contains some code snippets that were used to develop the script and analyze the replay files.

## How it works

The script parses the replay file and extracts the following information:

- the time when the player reached feudal age (from the chat messages and sync operations)
- the number of vils and techs queued up in a TC (from the actions)
- the number of vils and techs dequeued from a TC (from the actions)

Then, it calculates the idle time by adding up the build times of the queued vils and techs and subtracting the build times of the dequeued vils and techs. The result is compared to the time when the player reached feudal age.

## References
I could not find any comprehensive docs about the replay format. To fill this gap, I made a reference of the data I needed from in the replay files:
[REPLAY_DATA_REFERENCE.md](REPLAY_DATA_REFERENCE.md)

These resources proved useful: 

- the project is inspired by this (gist)[https://gist.github.com/santolucito/a01927be45a2a7a8e02ce9a50ddd8e75]
- the (outdated) docs for the aoe mgx format were useful: https://github.com/stefan-kolb/aoc-mgx-format
  - Events and their fields used in this project are described in [REPLAY_DATA_REFERENCE.md](REPLAY_DATA_REFERENCE.md)
- the [AoE2 DE replay parser](https://github.com/happyleavesaoc/aoc-mgz) is used here, the sources were useful reference.