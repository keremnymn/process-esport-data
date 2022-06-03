from app.tests import test_all_events, test_minion_kills, test_dragon_kills
import asyncio, argparse

if __name__ == "__main__":
    """
        To run the program, please provide an argument. For example:
            >>> python run.py --test all
        There are three arguments that can be provided:
            all: runs all the events in data folder.
            minions: runs random minion events and prints the players who killed minions
            dragons: runs all the dragon events and prints the teams that killed dragons
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", 
                        type=str,
                        required=True,
                        help="Please specify a test to run: all, minions, dragons")
    args = parser.parse_args()

    if args.test == "all":
        asyncio.run(test_all_events())
    elif args.test == "minions":
        asyncio.run(test_minion_kills())
    else:
        asyncio.run(test_dragon_kills())