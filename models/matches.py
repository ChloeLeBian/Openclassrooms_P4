from tinydb import TinyDB, Query


# 1 : initialiser TinyDB
db = TinyDB("database/database.json")

# 2 : définir une classe Match
class Match:
    def __init__(self, pair_of_players, score=[0, 0], tournoi=1):
        self.pair_of_players = pair_of_players
        self.score = score
        self.match = db.table("matches")
        self.tournoi = tournoi

    def get_pair_of_players(self):
        return self.pair_of_players

    def get_score(self):
        return self.score

    def set_score(self, score):
        self.score = score


# 3 : définir une classe MatchDB
class MatchDB:
    def __init__(self, current_tournament):
        self.current_tournament = current_tournament
        self.db = TinyDB(f"database/{current_tournament}.json")
        self.match = self.db.table("matches")

    def get_matches(self):
        matches = self.db.table("matches")
        return matches

    def query_match(self):
        match = Query()
        return match

    def initiate_score__matches(self, matches, match, elem):
        matches.update({"score": elem.get_score()}, match.score == [0.0, 0.0])

    def save_match(self, pair_of_players, score):
        self.match.insert(
            {"pair_of_players": pair_of_players, "score": score}
        )
        return {"pair_of_players": pair_of_players, "score": score}