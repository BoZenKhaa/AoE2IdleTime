# Needed replay format fields and their meaning

## Synchronization
SYNC

| Field | Type | Meaning                       |
| --- |---------------|-------------------------------|
| 0 | Integer       | Time increment in miliseconds |
| 1 | None, Integer | Unknown                       |
 

## Messaging

## Important Actions

DE_QUEUE - used for queueing units in buildings but not for techs.

| Field      | Type    | Meaning                                                                                                                 |
|------------|---------|-------------------------------------------------------------------------------------------------------------------------|
| player_id  | Integer | player id, 1-8                                                                                                          |
| object_ids | List    | List of object ids the action is performed on. For single TC, will be a list such as `[1960]`                           |
| amount     | Integer | Amount of units queued. For example, if you shift-queue 5 vils, this will be 5. Usually 1.                               |
| unit_id    | Integer | Unit id of the unit being queued. For example, 83 for villager.                                                          |
| sequence   | Integer | Sequence number of the action, as in all actions, not useful.                                 |

RESEARCH - used for queing tech research.

| Field      | Type    | Meaning                                                                                       |
|------------|---------|-----------------------------------------------------------------------------------------------|
| player_id  | Integer | player id, 1-8                                                                                |
| technology_id | Integer | Technology id of the tech being queued. For example, 22 for loom.                             |
| object_ids | List    | List of object ids the action is performed on. For single TC, will be a list such as `[1960]` |
| sequence   | Integer | Sequence number of the action, as in all actions, not useful.                                 |


SPECIAL - used for cancelling stuff from queues.

| Field      | Type    | Meaning                                                                                                                                                                                                                            |
|------------|---------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| player_id  | Integer | player id, 1-8                                                                                                                                                                                                                     |
| order_id   | Integer | subtype of action, see table below                                                                                                                                                                                                 |
| slot_id    | Integer | id of the queue slot that is being cancelled. Currently produced item is slot 0 (always single thing), stuff produced next is  slot 1 (e.g. 4 more vils), slot 2 is stuff queued after vils (e.g. loom), slot 3 can be vils again. |
| target_id  | Integer | probably -1 for all cancel actions                                                                                                                                                                                                 |
| x          | Float   | Probably x coordinate, not used in cancel actions                                                                                                                                                                                  |
| y          | Float   | Probably y coordinate, not used in cancel actions                                                                                                                                                                                  |
| object_ids | List    | List of object ids the action is performed on. For single TC, will be a list such as `[1960]`                                                                                                                                      |
| sequence   | Integer | Sequence number of the action, as in all action, not useful                                                                                                                                                                        |

| order_id | Meaning                                                                        |
|----------|--------------------------------------------------------------------------------|
| 4        | Cancel one item from the building queue                                        |
| 260      | Ctrl+Shift click top-left global queue icon (removes up to 5 items from queue) |



### Tidbits
 - Shift-queing 5 units at once does increases the `amount` field of the `ACTION` operation to 5.
 - 