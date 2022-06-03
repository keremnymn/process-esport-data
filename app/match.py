from datetime import datetime
from typing import List

import json, os, asyncio, logging

from app._dataclasses import Player, Team, Fixture
from app.event_handler import HandleEvents
from app.exceptions import TeamsLengthError, PlayersLengthError


async def load_json(json_file) -> dict:
    """
    loads the json file to a Python dictionary
    """
    with open(json_file, "r") as f:
        f = json.loads(f.read())
    return f


class Match:
    def __init__(self, start_file):
        # declare the teams. there will be 2 teams in total.
        self.teams: List[Team, Team] = []

        # parse the information
        self.match_info: dict = start_file
        self.id: str = self.match_info["matchID"]
        self.teams_info: list = self.match_info["payload"]["teams"]
        self.event_failures: int = 0
        self.winning_team: Team = None

        # add the fixture info to the class and add team informations
        self.save_fixture_info()
        self.add_teams_and_players()

        # start the event handler
        self.event_handler: HandleEvents = HandleEvents(self)

    def save_fixture_info(self) -> None:
        """
        stores fixture information to a Fixture object
        """
        payload = self.match_info["payload"]["fixture"]
        self.fixture = Fixture(
            seriesCurrent=payload["seriesCurrent"],
            seriesMax=payload["seriesMax"],
            seriesType=payload["seriesType"],
            title=payload["title"],
            startTime=datetime.strptime(payload["startTime"], "%Y-%m-%dT%H:%M:%SZ"),
        )

    def add_teams_and_players(self) -> None:
        """
        check the appropriate length of teams and players and add them to the Match object
        """
        try:
            if len(self.teams_info) != 2:
                raise TeamsLengthError("There should be two teams")
            for team in self.teams_info:
                if len(team["players"]) != 5:
                    raise PlayersLengthError("There should be 5 players in each team")
        except Exception as e:
            raise e

        names = ["Blue", "Red"]
        for index, team in enumerate(self.teams_info):
            this_team = Team(teamID=team["teamID"], name=names[index])
            for player in team["players"]:
                this_player = Player(name=player["name"])
                this_team.add_player(player["playerID"], this_player)
            self.teams.append(this_team)

    async def send_event(self, event) -> asyncio.coroutine:
        """
        Sends the dispatched event to the event_handler
        """
        try:
            event = await load_json(event)
            await self.event_handler.process_event(event)
        except json.JSONDecodeError:
            self.event_failures += 1
            logging.warning(f"Error parsing event: {os.path.split(event)[1]}")
