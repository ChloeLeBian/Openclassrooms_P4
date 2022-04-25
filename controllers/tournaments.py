from .globals import LIST_OF_MATCHES, NUMBER_OF_PLAYERS, NUMBER_MAX_OF_ROUNDS
from models import Tournament, tournament
from datetime import datetime


class ControllerTournaments:

    # 1 : récupérer la liste des matchs
    global list_of_matches
    list_of_matches = LIST_OF_MATCHES

    # 2 : récupérer le nombre de joueurs
    global number_of_players
    number_of_players = NUMBER_OF_PLAYERS

    # 3 : récupérer le nombre maximum de rounds
    global number_max_of_rounds
    number_max_of_rounds = NUMBER_MAX_OF_ROUNDS

    def __init__(self):
        pass
    
    # 4 : créer une fonction qui initialise le tournoi
    def start(self):
        """ 
        1 : checker si un tournoi existe
        2 : si un tournoi existe proposer de reprendre le tournoi ou de créer un nouveau tournoi
        3 : si il n'y a pas de tournoi existant créer un nouveau tournoi
        """
        # 1 : initialiser le nom du tournoi
        tournament_name = "database"
        # 2 : récupérer la liste des tournois grâce à la fonction get_tournaments dans models
        tournaments = self.models_tournament_db.get_tournaments()
        # 3 : si la liste des tournois est n'est pas vide
        if len(tournaments) > 0:
            # 1 : appeler la fonction view.deal_with_print dans vues pour notifier à l'organisateur
            # que des tournois existent déjà
            self.view.deal_with_print("un ou plusieurs tournoi(s) existe(nt) déjà\n")
            i = 0
            tournament_data = []
            # 2 : créer une boucle for pour afficher les tournois existant
            for tournament in tournaments:
                i = i+1
                tournament_data.append(tournament)
                self.view.deal_with_print(f"{i}. {tournament['name']}")
            # 3 : appeler la fonction view.deal_with_input dans vues pour notifier à l'organisateuret s'il veut revenir sur un des tournois
            # affichés ou en créer un nouveau et récupérer sa réponse
            answer = int(self.view.deal_with_input(f"choisir un tournoi dans la liste ci-dessus (de 1 à {i}) ou entez 0 pour créer un nouveau tournoi\n"))
            # 4 : si sa réponse est 0
            if answer == 0:
                # 1 : créer un nouveau tournoi en appelant la fonction create_tournament
                tournament_name = self.create_tournament()
            # 5 : sinon
            else:
                # 2 : aller chercher le nom du tournoi dans la liste des tournois selon sa réponse
                tournament_name = tournament_data[answer - 1]['name']
        
        # 4 : si la liste des tournois est vide
        else:
            # 1 : notifier à l'organisateur qu'il n'existe aucun tournoi
            self.view.deal_with_print("aucun tournoi n'existe il faut créer un nouveau tournoi\n")
            # 2 : appeler la fonction create_tournament pour créer un tournoi
            tournament_name = self.create_tournament()
        # 5 : afficher le nom du tournoi choisi ou créé
        self.view.deal_with_print(f"Le tournoi actuel est {tournament_name}\n")
        # 6 : récupérer le nom du tournoi
        return tournament_name

    # 5 : créer une fonction pour créer un tournoi
    def create_tournament(self):
        # 1 : demander à l'organisateur le nom du tournoi et le récupérer 
        name = self.view.deal_with_input(
                    "Entrez le nom du tournoi\n"
                )
        # 2 : demander à l'organisateur la date du tournoi et la récupérer 
        while True:
            try:
                date = self.view.deal_with_input(
                    "Entrez la date du tournoi au format dd/mm/yyyy:\n"
                )
                # 1 : vérifier le format de l'input
                dte = datetime.strptime(date, "%d/%m/%Y")
                date = dte
                # 2 : arrêter la boucle si le format est bon
                break
            # 2 : appeler la fonction view_deal_with_print dans Vues pour afficher la date entrée et notifier
            # à l'organisateur qu'il a entré un format invalide puis recommencer la boucle tant que
            # la date est incorrecte
            except ValueError as e:
                self.view.deal_with_print(e)
                self.view.deal_with_print("Format invalide")
        # 3 : demander à l'organisateur le lieu du tournoi et le récupérer 
        place = self.view.deal_with_input(
                    "Entrez le lieu du tournoi\n"
                )
        tournament = Tournament(
                name=name,
                date=date,
                place=place
            )
        # 4 : sauvegarer le tournoi
        tournament.save_tournament()
        # 5 : créer un nouveau json portant le nom du tournoi
        f = open(f"database/{name}.json", "w")
        # 6 : récupérer le nom du tournoi
        return name

    
    def step_four(self, list_of_matches):
    # 3 : appeler la fonction display ranking dans Vues qui permet d'afficher
    # les joueurs, leur score et leur rang
        pair_of_players = elem.get_pair_of_players()
        self.view.display_match_tournament(list_of_matches)


    