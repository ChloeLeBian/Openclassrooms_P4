from tinydb import TinyDB, Query


# 1 : initialiser TinyDB
db = TinyDB("database.json")

# 7 : définir une classe Tournament
class Tournament:
    def __init__(
        self, name, place, date, number_of_rounds, list_of_pairs_of_players, players
    ):
        self.name = name
        self.place = place
        self.date = date
        self.number_of_rounds = number_of_rounds
        self.list_of_pairs_of_players = list_of_pairs_of_players
        self.players = players

    def set_list_of_pairs_of_players(self, pair_of_players):
        self.list_of_pairs_of_players.append(pair_of_players)