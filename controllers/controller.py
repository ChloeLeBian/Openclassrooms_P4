from models import MatchDB, PlayerDB, TournamentDB
from vues import Vues
from .globals import LIST_OF_MATCHES, NUMBER_OF_PLAYERS, NUMBER_MAX_OF_ROUNDS
from .players import ControllerPlayers
from .matches import ControllerMatches
from .rounds import ControllerRounds
from .tournaments import ControllerTournaments


class Controller(ControllerPlayers, ControllerMatches, ControllerRounds, ControllerTournaments):

    # 1 : récupérer la liste des matchs
    global list_of_matches
    list_of_matches = LIST_OF_MATCHES

    # 2 : récupérer le nombre de joueurs
    global number_of_players
    number_of_players = NUMBER_OF_PLAYERS

    # 3 : récupérer le nombre maximum de rounds
    global number_max_of_rounds
    number_max_of_rounds = NUMBER_MAX_OF_ROUNDS

    # 4 : initialiser Vues, PlayerDB, MatchDB, TournamentDB et initialiser le tournoi
    def __init__(self):
        self.models_tournament_db = TournamentDB()
        self.view = Vues()
        self.current_tournament = self.start()
        self.models_player_db = PlayerDB(self.current_tournament)
        self.models_match_db = MatchDB(self.current_tournament)

    # 5 : définir une fonction menu
    def menu(self, list_of_players):

        # 1 : appeler la fonction view_deal_with_input dans Vues qui affiche du texte pour et récupère la réponse
        # de l'utilisateur pour afficher ses choix à l'organisateur
        answer = self.view.deal_with_input(
            "Ajouter joueurs: 1,\n\rGénérer round: 2,\n\rConsulter classement: 3,\n\rVisualisez rapport: 4\n "
        )
        # 2 : si son choix est 1
        if answer == "1":
            # 1 : appeler la fonction get_players dans models qui va chercher les joueurs dans Tinydb
            players = self.models_player_db.get_players()
            # 2 : appeler la fonction step_one qui défini ce qui se passe quand l'organisateur choisi 1
            self.step_one(len(players), list_of_players)
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
            )
        # 4 : si son choix est 3
        elif answer == "3":
            # 1 : appeler la fonction step qui défini ce qui se passe quand l'organisateur choisi 3
            self.step_three(list_of_players)
        # 5 : si son choix est 4
        elif answer == "4":
            # 1 : appeler la fonction view_deal_with_print dans Vues qui affiche du texte notifier
            # à l'utilisateur ce que la fonction suivante va afficher
            self.view.deal_with_print("\nListe des joueurs classés par score\n")
            # 2 : appeler la fonction rank_players_by_score qui classe les joueurs selon leur score
            self.rank_players_by_score()
            # 3 : appeler la fonction get_all_matches dans models qui va chercher les matchs dans Tinydb
            list_of_matches = self.models_match_db.get_all_matches()
            # 4 : appeler la fonction step_four qui défini le reste de ce qui se passe quand l'organisateur choisi 4
            self.step_four(list_of_matches)
        # 6 : sinon
        else:
            # 1 : appeler la fonction view_deal_with_print dans Vues qui affiche
            # du texte pour notifier à l'organisateur que son choix est incorrect
            self.view.deal_with_print("Veuillez entrer 1, 2, ou 3")
            # 2 : retourner le menu
            return self.menu(list_of_players)

    # 6 : définir une fonction qui permet de vérifier si un élément est un float
    def isfloat(self, num):
        try:
            float(num)
            return True
        except ValueError:
            return False

    # 7 : définir une fonction qui permet de vérifier si un élément est un entier
    def isint(self, num):
        try:
            int(num)
            return True
        except ValueError:
            return False

    # 8 : définir une fonction qui permet de vérifier si un élément valide en étant un entier situé entre
    # 1 et la longueur d'une liste
    def numberisvalid(self, num, number_of_elements):
        if not self.isint(num):
            return False
        if int(num) < 1 or int(num) > number_of_elements:
            return False
        return True
