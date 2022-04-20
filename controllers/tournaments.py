from .globals import LIST_OF_MATCHES, NUMBER_OF_PLAYERS, NUMBER_MAX_OF_ROUNDS
from models import Tournament, tournament
from datetime import datetime


class ControllerTournaments:

    global list_of_matches
    list_of_matches = LIST_OF_MATCHES

    # 2 : définir le nombre de joueurs
    global number_of_players
    number_of_players = NUMBER_OF_PLAYERS

    # 3 : définir le nombre maximum de rounds
    global number_max_of_rounds
    number_max_of_rounds = NUMBER_MAX_OF_ROUNDS

    def __init__(self):
        pass

    def start(self):
        """ 
        1 : checker si un tournoi existe
        2 : si un tournoi existe proposer de reprendre le tournoi ou de créer un nouveau tournoi
        3 : si il n'y a pas de tournoi existant créer un nouveau tournoi
        """
        tournament_name = "database"
        tournaments = self.models_tournament_db.get_tournaments()
        if len(tournaments) > 0:
            print("un ou plusieurs tournoi(s) existe(nt) déjà\n")
            i = 0
            tournament_data = []
            for tournament in tournaments:
                i = i+1
                tournament_data.append(tournament)
                print(f"{i}. {tournament['name']}")
            answer = int(input(f"choisir un tournoi dans la liste ci-dessus (de 1 à {i}) ou entez 0 pour créer un nouveau tournoi\n"))
            if answer == 0:
                tournament_name = self.create_tournament()
            else:
                tournament_name = tournament_data[answer - 1]['name']

        else:
            print("aucun tournoi n'existe il faut créer un nouveau tournoi\n")
            tournament_name = self.create_tournament()
        print(f"Le tournoi actuel est {tournament_name}\n")
        return tournament_name

    def create_tournament(self):
        name = self.view.deal_with_input(
                    "Entrez le nom du tournoi\n"
                )
        while True:
            try:
                date = self.view.deal_with_input(
                    "Entrez la date du tournoi au format dd/mm/yyyy:\n"
                )
                # 2 : vérifier le format de l'input
                dte = datetime.strptime(date, "%d/%m/%Y")
                date = dte
                # 3 : arrêter la boucle si le format est bon
                break
            # 2 : appeler la fonction view_deal_with_print dans Vues pour afficher la date entrée et notifier
            # à l'organisateur qu'il a entré un format invalide puis recommencer la boucle tant que
            # la date est incorrecte
            except ValueError as e:
                self.view.deal_with_print(e)
                self.view.deal_with_print("Format invalide")
        place = self.view.deal_with_input(
                    "Entrez le lieu du tournoi\n"
                )
        tournament = Tournament(
                name=name,
                date=date,
                place=place
            )
        tournament.save_tournament()
        f = open(f"database/{name}.json", "w")
        return name

    