from models import MatchDB, PlayerDB
from vues import Vues
from .globals import LIST_OF_MATCHES, NUMBER_OF_PLAYERS, NUMBER_MAX_OF_ROUNDS
from .players import ControllerPlayers
from .matches import ControllerMatches
from .rounds import ControllerRounds


class Controller(ControllerPlayers, ControllerMatches, ControllerRounds):

    # 1 : ouvrir la liste des matchs
    global list_of_matches
    list_of_matches = LIST_OF_MATCHES

    # 2 : définir le nombre de joueurs
    global number_of_players
    number_of_players = NUMBER_OF_PLAYERS

    # 3 : définir le nombre maximum de rounds
    global number_max_of_rounds
    number_max_of_rounds = NUMBER_MAX_OF_ROUNDS

    # 4 : initialiser Vues, PlayerDB et MatchDB
    def __init__(self):
        self.view = Vues()
        self.models_player_db = PlayerDB()
        self.models_match_db = MatchDB()

    # 5 : définir une fonction menu
    # Controller
    def menu(self, list_of_players, list_of_pairs_of_players):
        # 1 : appeler la fonction view_deal_with_input dans Vues qui affiche du texte pour et récupère la réponse
        # de l'utilisateur pour afficher ses choix à l'organisateur
        answer = self.view.deal_with_input(
            "Ajouter des joueurs: 1,  \n\rGénérer un round: 2,\n\rConsulter le classement des joueurs: 3,\n "
        )
        # 2 : si son choix est 1
        if answer == "1":
            # 1 : appeler la fonction get_players dans models qui va chercher les joueurs dans Tinydb
            players = self.models_player_db.get_players()
            # 2 : appeler la fonction step_one qui défini ce qui se passe quand l'organisateur choisi 1
            self.step_one(len(players), list_of_players, list_of_pairs_of_players)
        # 3 : si son choix est 2
        elif answer == "2":
            # 1 : appeler la fonction get_players dans models qui va chercher les joueurs dans Tinydb
            players = self.models_player_db.get_players()
            # 2 : appeler la fonction get_matches dans models qui va chercher les matchs dans Tinydb
            matches = self.models_match_db.get_matches()
            # 3 : créer une liste des joueurs à partir des joueurs récupérés dans Tinydb au préalable
            list_of_players = players.all()
            # 4 : regarder la longueur de la liste pour calculer le nombre de joueurs
            nb_of_players = len(list_of_players)
            # 5 : calculer le nombre de rounds possible à partir du nombre de joueurs
            nb_of_rounds = int(nb_of_players - 1)
            # 6 : appeler la fonction step_two qui défini ce qui se passe quand l'organisateur choisi 2
            self.step_two(
                len(players),
                nb_of_players,
                nb_of_rounds,
                matches,
                list_of_players,
                list_of_pairs_of_players,
            )
        # 4 : si son choix est 3
        elif answer == "3":
            # 1 : appeler la fonction rank_players qui classe les joueurs selon leur score
            self.rank_players()
            # 2 : retourner le menu
            return self.menu(list_of_players, list_of_pairs_of_players)
        # 5 : si son choix n'est pas compris dans les choix proposés
        else:
            # 1 : appeler la fonction view_deal_with_print dans Vues qui affiche
            # du texte pour notifier à l'organisateur que son choix est incorrect
            self.view.deal_with_print("Veuillez entrer 1, 2, ou 3")
            # 2 : retourner le menu
            return self.menu(list_of_players, list_of_pairs_of_players)

    # 13 : définir une fonction qui permet de créer une liste de paires de joueurs
    # Controller?
    def create_list_of_pairs_of_players(
        self, list_of_matches, list_of_pairs_of_players
    ):
        # 1 : faire une boucle pour tous les matchs dans la liste de matchs
        for elem in list_of_matches:
            # 1 : récupérer la paire de joueur du match
            pair_of_players = elem.get_pair_of_players()
            # 2 : ajouter le nom de famille des joueurs à la liste de paires de joueurs
            list_of_pairs_of_players.append(
                (
                    pair_of_players[0]["family_name"],
                    pair_of_players[1]["family_name"],
                )
            )
        # 2 : récupérer la liste de paires de joueurs complétée
        return list_of_pairs_of_players

    # 15 : définir une fonction qui permet de vérifier si un élément est un float
    # Controller?
    def isfloat(self, num):
        try:
            float(num)
            return True
        except ValueError:
            return False

    # 16 : définir une fonction qui permet de vérifier si un élément est un entier
    # Controller?
    def isint(self, num):
        try:
            int(num)
            return True
        except ValueError:
            return False

    # 17 : définir une fonction qui permet de vérifier si un élément valide en étant un entier situé entre
    # 1 et la longueur d'une liste
    # Controller?
    def numberisvalid(self, num, number_of_elements):
        if not self.isint(num):
            return False
        if int(num) < 1 or int(num) > number_of_elements:
            return False
        return True
