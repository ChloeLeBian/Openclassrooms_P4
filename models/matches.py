from tinydb import TinyDB, Query


# 1 : initialiser TinyDB
db = TinyDB("database.json")

# 2 : définir une classe Match
class Match:
    def __init__(self, pair_of_players, score=[0, 0]):
        self.pair_of_players = pair_of_players
        self.score = score
        self.match = db.table("matches")

    def get_pair_of_players(self):
        return self.pair_of_players

    def get_score(self):
        return self.score

    def set_score(self, score):
        self.score = score

    def save_match(self):
        self.match.insert(
            {"pair_of_players": self.pair_of_players, "score": self.score}
        )
        return {"pair_of_players": self.pair_of_players, "score": self.score}


# 3 : définir une classe MatchDB
class MatchDB:
    def __init__(self):
        pass

    def get_matches(self):
        matches = db.table("matches")
        return matches

    def query_match(self):
        match = Query()
        return match

    def initiate_score__matches(self, matches, match, elem):
        matches.update({"score": elem.get_score()}, match.score == [0.0, 0.0])
