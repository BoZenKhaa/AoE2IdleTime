import ast
import logging
from typing import Any
from dataclasses import dataclass

from aoe2_constants import Ages, EntityIDs, TRACKED_TECHNOLOGIES, BUILD_TIMES
from mgz import fast
from mgz.fast import Operation
from datetime import timedelta

@dataclass
class TimedAction:
    time: int
    action: Operation
    payload: Any

    def get_payload_string(self):
        if self.action == fast.Action.DE_QUEUE:
            return f"Queue {self.payload['unit_id']}"
        if self.action == fast.Action.RESEARCH:
            return f"Research {self.payload['technology_id']}"
        if self.action == fast.Action.SPECIAL:
            return f"Cancel with {self.payload['order_id']} in slot {self.payload['slot_id']}"

    def __str__(self):
        return f"{timedelta(milliseconds=self.time)} {self.get_payload_string()}"

    def __repr__(self):
        return self.__str__()


class PlayerAgeInfo:
    player_id: int
    current_age: Ages
    queue: dict[Ages, list[int]]
    age_time: dict[Ages, int]
    tc_ids = set[int]

    def __init__(self, player_id):
        self.player_id = player_id
        self.current_age = Ages.DARK
        self.queue = {Ages.DARK: [], Ages.FEUDAL: [], Ages.CASTLE: [], Ages.IMPERIAL: []}
        self.age_time = {Ages.DARK: 0, Ages.FEUDAL: None, Ages.CASTLE: None, Ages.IMPERIAL: None}
        self.tc_ids = set()

    def is_empty(self):
        return len(self.tc_ids) == 0


def get_age_up_from_chat(chat):
    payload = ast.literal_eval(chat.decode("utf-8"))
    if payload["message"].endswith("advanced to the Feudal Age."):
        return payload["player"], Ages.FEUDAL
    elif payload["message"].endswith("advanced to the Castle Age."):
        return payload["player"], Ages.CASTLE
    elif payload["message"].endswith("advanced to the Imperial Age."):
        return payload["player"], Ages.IMPERIAL
    else:
        return None, None


def gather_tc_events_from_game_data(game_data):
    """
    Build TC queue for each player from game data. Generated queues contain built vils, researched techs and cancel actions.
    """
    t = 0
    player_tc_queues = [PlayerAgeInfo(i) for i in range(1, 9)]  # max 8 players, indexed by player_id-1
    for op_type, event in game_data:
        if op_type == Operation.SYNC:
            td = event[0]
            t += td
        elif op_type == Operation.ACTION:
            action, payload = event
            player_info = player_tc_queues[payload["player_id"] - 1]
            if action == fast.Action.DE_QUEUE and payload["unit_id"] == EntityIDs.VILLAGER.value:
                player_info.queue[player_info.current_age].append(TimedAction(t, action, payload))
                player_info.tc_ids = player_info.tc_ids.union(payload["object_ids"])
            if action == fast.Action.RESEARCH and payload["technology_id"] in map(lambda e: e.value,
                                                                                  TRACKED_TECHNOLOGIES):
                player_info.queue[player_info.current_age].append(TimedAction(t, action, payload))
            # Potentially a cancel action
            elif action == fast.Action.SPECIAL:
                if payload["order_id"] in [4, 260] and payload["target_id"] == -1 and player_info.tc_ids.intersection(
                        payload["object_ids"]):
                    player_info.queue[player_info.current_age].append(TimedAction(t, action, payload))

        elif op_type == Operation.CHAT:
            player_id, age = get_age_up_from_chat(event)
            if player_id is not None:
                player_tc_queues[player_id - 1].current_age = age
                player_tc_queues[player_id - 1].age_time[age] = t
                logging.debug(f"{t}ms, player {player_id}, {age}, {timedelta(milliseconds=t)}")
            else:
                logging.debug(f"{t}ms, chat:{event}, {timedelta(milliseconds=t)}")

    return player_tc_queues


FEUDAL_RESEARCH_EPSILON=1000 #
def dark_age_idle_time(player_info: PlayerAgeInfo):
    """
    Proof of concept for the dark age idle time calculation.

    Rules:
      - cancellations AFTER starting researching last feudal are not relevant
      - cancellations BEFORE starting researching last feudal are
      - stuff in queue before last feudal research is relevant
      - stuff in queue after last feudal research is not relevant

    The function does following:
    - get a list of queued vils, techs and cancellations before the feudal research actually started
      - we get this by looking at the timestamp of reaching feudal minus the time it takes to research feudal, removing anything after such time.
    - in this list, we remove queued up techs and vils after the last feudal research, but not cancellations.
    - then, we add up count of vills and techs, feudal researches and cancellations. We subtract fedual reserarches -1 from cancellations and then the cancellations from queued up vills and techs.
    - finally, we multiply the queued up count by build time to get effective tc "busy" time.
    """
    dark_age_queue = player_info.queue[Ages.DARK]

    feudal_research_start_time = player_info.age_time[Ages.FEUDAL] - BUILD_TIMES[EntityIDs.FEUDAL_AGE.value]

    queue_before_starting_feudal_research = list(filter(lambda ta: ta.time <= feudal_research_start_time + FEUDAL_RESEARCH_EPSILON,
                                                        dark_age_queue))  # If feudal message is sent after reaching feudal, then this should always include the last feudal research as well. TODO: confirm this

    feudal_research_queue_indeces = []
    for i, ta in enumerate(queue_before_starting_feudal_research):
        if ta.action == fast.Action.RESEARCH and ta.payload["technology_id"] == EntityIDs.FEUDAL_AGE.value:
            feudal_research_queue_indeces.append(i)

    feudal_tech_queue_index = feudal_research_queue_indeces[-1]
    unfinished_feudal_research_count = len(feudal_research_queue_indeces) - 1 # 1 for the finished research

    relevant_queued_vill_count = 0
    relevant_queued_loom_count = 0
    relevant_cancellations = 0
    for i, ta in enumerate(queue_before_starting_feudal_research):
        if ta.action == fast.Action.DE_QUEUE and i < feudal_tech_queue_index:  # Could be only vil
            relevant_queued_vill_count += 1
        if ta.action == fast.Action.RESEARCH and ta.payload[
            "technology_id"] == EntityIDs.LOOM.value and i < feudal_tech_queue_index:
            relevant_queued_loom_count += 1
        if ta.action == fast.Action.SPECIAL:
            relevant_cancellations += 1

    logging.info(
        f"Dark age queue:\n vils: {relevant_queued_vill_count},\n loom: {relevant_queued_loom_count},\n unfinished feudal researches: {unfinished_feudal_research_count},\n cancellations: {relevant_cancellations}")

    tc_dark_busy_time = (
                                relevant_queued_loom_count + relevant_queued_vill_count + unfinished_feudal_research_count - relevant_cancellations) * \
                        BUILD_TIMES[EntityIDs.VILLAGER.value]

    idle_time_dark = player_info.age_time[Ages.FEUDAL] - tc_dark_busy_time
    logging.info(f"Dark age idle time: {timedelta(milliseconds=idle_time_dark)}")
    return idle_time_dark


if __name__ == '__main__':
    from utils import load_replay

    logging.basicConfig(level=logging.INFO)

    REPLAY = 'data/SP_timed_replay.aoe2record'

    game_data = load_replay(REPLAY)
    player_infos = gather_tc_events_from_game_data(game_data)
    for pi in player_infos:
        if not pi.is_empty():
            logging.info(f"Player {pi.player_id} idle time:")
            dark_age_idle_time(pi)
