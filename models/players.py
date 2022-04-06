from tinydb import TinyDB, Query


# 1 : initialiser TinyDB
db = TinyDB("database.json")


# 4 : définir une classe Player
class Player:
    def __init__(
        self, family_name, surname, date_of_birth, sex, ranking, score, total_score=0
    ):
        self.family_name = family_name
        self.surname = surname
        self.date_of_birth = date_of_birth
        self.sex = sex
        self.ranking = ranking
        self.score = score
        self.total_score = total_score

    def get_family_name(self):
        return self.family_name

    def set_family_name(self, new_family_name):
        self.family_name = new_family_name

    def get_surname(self):
        return self.surname

    def set_surname(self, new_surname):
        self.surname = new_surname

    def get_date_of_birth(self):
        return self.date_of_birth

    def set_date_of_birth(self, new_date):
        self.date_of_birth = new_date

    def get_sex(self):
        return self.sex

    def set_sex(self, new_sex):
        self.sex = new_sex

    def get_ranking(self):
        return self.ranking

    def set_ranking(self, new_ranking):
        self.ranking = new_ranking

    def get_score(self):
        return float(self.total_score)

    def calculate_score(self, new_score):
        self.total_score = new_score


# 5 : définir une classe PlayerDB
class PlayerDB:
    def __init__(self):
        pass

    def get_players(self):
        players = db.table("players")
        return players

    def save_players(self, list_of_players):
        players = db.table("players")
        for elem in list_of_players:

            players.insert(
                {
                    "surname": elem.get_surname(),
                    "family_name": elem.get_family_name(),
                    "date_of_birth": str(elem.get_date_of_birth()),
                    "sex": elem.get_sex(),
                    "ranking": elem.get_ranking(),
                    "score": elem.get_score(),
                }
            )

    def query_player(self):
        player = Query()
        return player

    def search_player(self, player, players, family_name):
        current_player = players.search(player.family_name == family_name)
        return current_player

    def search_player_p2(self, player, players, family_name):
        p2 = players.search(player.family_name == family_name)
        return p2

    def update_score_player(self, player, players, current_score, family_name):
        players.update({"score": current_score}, player.family_name == family_name)