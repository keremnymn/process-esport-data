from app.exceptions import InvalidPlayerID, InvalidEventType, InvalidTeamID
from app._dataclasses import Turret, Dragon, Player, Team
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s:%(levelname)s:%(name)s:%(message)s"
)


class HandleEvents:
    def __init__(self, match):
        self.match = match
        self.event_mapping = {
            "PLAYER_REVIVE": [0, self.handle_player_revive],
            "NASHOR_KILL": [0, self.handle_nashor_kill],
            "MINION_KILL": [0, self.handle_minion_kill],
            "MATCH_END": [0, self.handle_match_end],
            "TURRET_DESTROY": [0, self.handle_turret_destroy],
            "PLAYER_KILL": [0, self.handle_player_kill],
            "UNKNOWN": [0, self.handle_unknown],
            "DRAGON_KILL": [0, self.handle_dragon_kill],
        }

    async def get_player(self, id: str):
        """
        Returns the player and the team that the player belongs to
        """
        player: Player = None
        team: Team = None
        for team in self.match.teams:
            if id in team.players:
                player = team.players[id]
                team = team
                break

        if not player:
            raise InvalidPlayerID(f"Player with ID {id} can not be found.")

        return player, team

    async def get_team(self, id: str):
        """
        Returns the team when the player is unknown
        """
        team: Team = None
        for _team in self.match.teams:
            if _team.teamID == id:
                team = _team

        if not team:
            raise InvalidTeamID(f"Team with ID {id} can not be found")

        return team

    async def process_event(self, event: dict) -> None:
        """
        Processes the received event with the corresponding function and counts the successful events
        """
        if event["type"] == "MATCH_START":
            pass
        elif event["type"] not in self.event_mapping:
            raise InvalidEventType("Event type is not valid: %s" % (event["type"],))
        else:
            try:
                # dispatch the event to corresponding function
                await self.event_mapping[event["type"]][1](event)

                # if the function is successful, count the event
                self.event_mapping[event["type"]][0] += 1
            except Exception as e:
                raise e

    async def handle_player_revive(self, event) -> None:
        player, _ = await self.get_player(event["payload"]["playerID"])
        player.alive = True

    async def handle_nashor_kill(self, event) -> None:
        player, team = await self.get_player(event["payload"]["killerID"])

        # 300 Gold to each team member
        for player in team.players.values():
            player.gold += event["payload"]["teamGoldGranted"]

        team.nashorKills += 1
        logging.info(f"{team.name} Team has slain the Nashor!")

    async def handle_minion_kill(self, event) -> None:
        player, _ = await self.get_player(event["payload"]["playerID"])
        player.gold += event["payload"]["goldGranted"]
        player.minions += 1
        # no need to announce the minion kill

    async def handle_match_end(self, event) -> None:
        team = await self.get_team(event["payload"]["winningTeamID"])
        self.match.winning_team = team
        logging.info(f"{team.name} Team has won!")

    async def handle_turret_destroy(self, event) -> None:
        skipPlayer = None
        if event["payload"]["killerID"]:

            player, team = await self.get_player(event["payload"]["killerID"])
            player.gold += event["payload"]["playerGoldGranted"]

            # this player already got a reward, so we should skip it.
            skipPlayer = player

        else:
            team = await self.get_team(event["payload"]["killerTeamID"])

        # create a tower object and store it in team object
        tower = Turret(event["payload"]["turretTier"], event["payload"]["turretLane"])
        team.destroyed_turrets.append(tower)

        players = [player for player in team.players.values()]

        # reward all the players except for the one who already got a reward.
        for player in players:
            if player != skipPlayer:
                player.gold += event["payload"]["teamGoldGranted"]

        logging.info(f"{team.name} Team has destroyed a {tower}.")

    async def handle_player_kill(self, event):
        killer = event["payload"]["killerID"]
        if killer:
            player, team = await self.get_player(killer)
            player.kills += 1
            player.gold += event["payload"]["goldGranted"]

            if not self.event_mapping["PLAYER_KILL"][0]:
                logging.info(f"First blood: {player.name}")

        assistants = event["payload"]["assistants"]
        if assistants:
            for assistant_id in assistants:
                assistant, _ = await self.get_player(assistant_id)
                assistant.assists += 1
                assistant.gold += event["payload"]["assistGold"]

        victim, _ = await self.get_player(event["payload"]["victimID"])
        victim.deaths += 1
        victim.alive = False

    async def handle_unknown(self, event) -> None:
        pass

    async def handle_dragon_kill(self, event) -> None:
        player, team = await self.get_player(event["payload"]["killerID"])
        dragon = Dragon(event["payload"]["dragonType"])
        team.killed_dragons.append(dragon)

        for player in team.players.values():
            player.gold += event["payload"]["goldGranted"]

        logging.info(f"{team.name} Team has slain the dragon!")
