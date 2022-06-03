# Coding Challenge

## Part 1: Event parser

Create a game state handler for league of legends that can process multiple types of
events and update the current status accordingly. The implementation should keep track of
all the variables that represent the state of the game at any given time, and update the
relevant ones as needed.

Events are represented as a dictionary containing the event type, and a payload, which is
another dictionary with the specific information about this event.

```json
{
    "type": "MATCH_EVENT",
    "payload": {
        "field1": "value",
        "field2": "value2",
    }
}
```

Events have different meanings based on their type, and their payloads can have different
fields depending on the information they need to convey. However, all events of one type
are always guaranteed to have the same set of fields.

Below is a description of each of the event types, and their expected effect:

* `MATCH_START`: Initializes a new game state. Contains all the initial information about
  the game, the teams and their players. This event is always guaranteed to arrive first.
* `MINION_KILL`: A player killed a minion. The player is granted some gold and their
  minion count is updated.
* `PLAYER_KILL`: One player killed another, optionally assisted by other members of the
  team. The killer is granted some gold, and each of the assistants receive a reduced
  amount. Kills, deaths and assists stats should be updated for all the players involved.
* `PLAYER_REVIVE`: A previously killed player respawned back into the game. Its alive
  status should be updated.
* `DRAGON_KILL`: One player killed a dragon. The team's dragon kill count should be
  updated, and the player is granted some gold.
* `NASHOR_KILL`: One player killed Baron Nashor. The team's nashor kill count should be
  updated, plus every member of the team receives the specified amount of gold.
* `TURRET_DESTROY`: A team destroyed an enemy turret. The team's tower kill count should
  be updated, and each of its players receives some gold. Additionally, the player who
  took the tower receives `playerGoldGranted` gold. Keep in mind that sometimes towers
  are destroyed by minions, so no individual player receives `playerGold`, although team
  gold is still granted.
* `MATCH_END`: The match ended, and a winner is declared. There are never any events
  after this one.

Watch out for events that are unparsable or have incomplete information. In those cases
you should do your best to update the gamestate with the information that you have, or
skip them altogether if they are completely unusable.

To complete part 1 of this challenge, write a parser that can process each event in the
`data/` directory individually, and update the game state accordingly. You are free to
create any files and use external libraries if needed.

## Part 2: Testing
Write tests that verify the behavior of your implementation.

We don't expect full coverage, but there should be enough tests to ensure that the
processing of events is working as expected. The `samples/` directory contains one event
of each type in separate files to make this process a bit easier.

While pytest is encouraged, you are allowed to use other frameworks of your choice.
