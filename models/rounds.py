from tinydb import TinyDB


# 1 : initialiser TinyDB
db = TinyDB("database.json")

# 6 : définir une classe Round
class Round:
    def __init__(self, name, matches):
        self.name = name
        self.matches = matches

    def get_round_name(self):
        return self.name

    def get_list_of_matches(self):
        return self.matches
