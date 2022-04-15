from tinydb import TinyDB


# 1 : initialiser TinyDB
db = TinyDB("database/tournaments.json")

# 7 : définir une classe Tournament
class Tournament:
    def __init__(self, name, place, date):
        self.name = name
        self.place = place
        self.date = date
        self.tournament = db.table("tournaments")

    def save_tournament(self):
        self.tournament.insert({"name": self.name, "place": self.place, "date": str(self.date)})
        return {"name": self.name, "place": self.place, "date": self.date}

    
class TournamentDB:
    def __init__(self):
        pass

    def get_tournaments(self):
        tournaments = db.table("tournaments")
        return tournaments