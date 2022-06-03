import os, asyncio, random
from app.match import Match, load_json

current_dir = os.getcwd().replace("/app", "/")


async def dispatch_event(match, event) -> asyncio.coroutine:
    await match.send_event(event)


async def start_the_game() -> Match:
    start_info = os.path.join(current_dir, "samples/match_start.json")
    start_info = await load_json(start_info)

    match = Match(start_info)
    return match


async def has_type(file_path: os.PathLike, keyword: str) -> bool:
    with open(file_path, "r") as f:
        f = f.read()
    return keyword in f


async def test_all_events():
    """
    Dispatches all the events in samples/ and checks the following:
        broken_files,
        winning team,
        total_kills,
        minion_kills,
        red_team_dragon_kills,
        blue_team_towers_destroyed,
        best_player_by_kills
    """
    m = await start_the_game()

    end = ""
    for event_file in os.listdir(os.path.join(current_dir, "data")):
        e = os.path.join(current_dir, "data", event_file)
        if await has_type(e, "MATCH_END"):
            end = e
            continue
        await dispatch_event(m, e)

    # to make sense, run the match_end event at the end of the loop
    await dispatch_event(m, end)

    broken_files = 4
    assert broken_files == m.event_failures
    assert m.winning_team.name == "Red"

    total_kills = 25
    assert m.event_handler.event_mapping["PLAYER_KILL"][0] == total_kills

    minion_kills = 669
    assert m.event_handler.event_mapping["MINION_KILL"][0] == minion_kills

    red_team_dragon_kills = 4
    assert m.teams[1].dragonKills == red_team_dragon_kills

    blue_team_towers_destroyed = 4
    assert m.teams[0].towersDestroyed == blue_team_towers_destroyed

    best_player_by_kills = (7, "G2 caPs")
    best_player_in_match = (0, None)

    for team in m.teams:
        for player in team.players.values():
            if player.kills > best_player_in_match[0]:
                best_player_in_match = (player.kills, player.name)

    assert best_player_in_match == best_player_by_kills


async def test_minion_kills():
    m = await start_the_game()

    random_minion_events = [random.randint(0, 740) for iter in range(10)]
    for e in random_minion_events:
        e = os.path.join(current_dir, "data", str("%03d" % (e,)) + ".json")
        if not await has_type(e, "MINION_KILL"):
            continue
        await dispatch_event(m, e)

    print("Players who killed minions: ")
    for team in m.teams:
        for player in team.players.values():
            if player.minions:
                print(
                    player.name,
                    "-- killed minions: ",
                    player.minions,
                    "-- gold: ",
                    player.gold,
                )


async def test_dragon_kills():
    m = await start_the_game()

    for e in os.listdir(os.path.join(current_dir, "data")):
        e = os.path.join(current_dir, "data", e)
        if not await has_type(e, "DRAGON_KILL"):
            continue
        await dispatch_event(m, e)

    for team in m.teams:
        if team.killed_dragons:
            print(team.killed_dragons)
