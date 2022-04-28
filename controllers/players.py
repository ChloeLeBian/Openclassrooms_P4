from datetime import datetime
from .globals import LIST_OF_MATCHES, NUMBER_OF_PLAYERS, NUMBER_MAX_OF_ROUNDS
from models import Player


class ControllerPlayers:

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

    # 4 : définir une fonction détaillant ce qui se passe quand on choisi 1 dans le menu
    def step_one(self, x, list_of_players):
        # 1 : si la liste des joueurs dans Tinydb est vide
        if x == 0:
            # 1 : appeler la fonction create_players pour créer les joueurs
            list_of_players = self.create_players(number_of_players)
            # 2 : appeler la fonction save_players pour sauvegarder les joueurs
            self.save_players(list_of_players)
            # 3 : retourner le menu
            return self.menu(list_of_players)

        # 2 : si la liste des joueurs dans Tinydb n'est pas vide
        else:
            # 1 : appeler la fonction view_deal_with_print dans Vues pour notifier à l'organisateur
            # qu'il a déjà enregistré ses joueurs
            self.view.deal_with_print(
                "Vous avez déjà enregistrés vos joueurs, veuillez générer vos rounds\n\r"
            )
            # 2 : retourner le menu
            return self.menu(list_of_players)

    # 5 : définir une fonction détaillant ce qui se passe quand on choisi 3 dans le menu
    def step_three(self, list_of_players):
        # 1 : appeler la fonction view_deal_with_input dans Vues pour affichez ses choix à l'organisateur et récupérer
        # sa réponse
        answer = self.view.deal_with_input("Classer par score: 1,\n\rClasser par ordre alphabétique: 2\n\r")
        # 2 : si sa réponse est 1
        if answer == "1":
            # 1 : appeler la fonction rank_players_by_score qui classe les joueurs selon leur score
            self.rank_players_by_score()
            # 2 : retourner le menu
            return self.menu(list_of_players)
        # 3 : si sa réponse est 2
        elif answer == "2":
            # 1 : appeler la fonction rank_players_by_name qui classe les joueurs selon leur nom de famille
            self.rank_players_by_name()
            # 2 : retourner le menu
            return self.menu(list_of_players)
        # 4 : sinon
        else:
            # 1 : appeler la fonction view_deal_with_print dans Vues qui affiche
            # du texte pour notifier à l'organisateur que son choix est incorrect
            self.view.deal_with_print("Veuillez entrer 1 ou 2")
            # 2 : retourner le menu
            return self.step_three(list_of_players)

    # 6 : définir une fonction qui permet de classer les joueurs selon leur score par ordre décroissant
    def rank_players_by_score(self):
        # 1 : appeler la fonction get_players dans Models qui permet de récupérer les joueurs dans TinyDB
        # et les mettre dans une liste de joueurs
        list_of_players = self.models_player_db.get_players()
        # 2 : classer les joueurs de la liste selon leur score
        list_of_players = sorted(
            list_of_players, key=lambda d: d["score"], reverse=True
        )
        # 3 : appeler la fonction display ranking dans Vues qui permet d'afficher
        # les joueurs, leur score et leur rang
        self.view.display_ranking(list_of_players)

    # 7 : définir une fonction qui permet de classer les joueurs selon leur nom par ordre croissant
    def rank_players_by_name(self):
        # 1 : appeler la fonction get_players dans Models qui permet de récupérer les joueurs dans TinyDB
        # et les mettre dans une liste de joueurs
        list_of_players = self.models_player_db.get_players()
        # 2 : classer les joueurs de la liste selon leur nom de famille par ordre croissant
        list_of_players = sorted(
            list_of_players, key=lambda d: d["family_name"], reverse=False
        )
        # 3 : appeler la fonction display ranking dans Vues qui permet d'afficher
        # les joueurs, leur score et leur rang
        self.view.display_ranking(list_of_players)

    # 8 : définir une fonction qui permet de créer des joueurs en fonction du
    # nombre de joueurs défini
    def create_players(self, number_of_players):
        # 1 : initaliser une liste de joueurs
        players = []
        # 2 : initialiser une liste des rangs des joueurs
        rankings_players = []
        # 3 : définir une boucle allant de 0 au nombre de joueurs choisi au début
        for i in range(1, number_of_players + 1):
            # 1 : aller chercher les informations de chaque joueur grâce à la fonction
            # get_info_of_players
            (
                surname,
                family_name,
                date_of_birth,
                sex,
                ranking,
                score,
            ) = self.get_info_of_player(rankings_players, i)
            # 2 : ajouter le ranking du joueur à la liste de ranking
            rankings_players.append(ranking)
            # 3 : définir chaque joueur comme un dictionnaire d'informations
            player = Player(
                family_name=family_name,
                surname=surname,
                date_of_birth=date_of_birth,
                sex=sex,
                ranking=ranking,
                score=score,
            )
            # 4 : ajouter chaque joueur à la liste des joueurs
            players.append(player)
        # 4 : retourner la liste des joueurs classés selon leur rang par ordre croissant
        return sorted(players, key=lambda player: player.ranking)

    # 9 : définir une fonction qui permet de récupérer les informations d'un joueur n°i
    def get_info_of_player(self, rankings_players, i):
        # 1 : appeler la fonction view_deal_with_input dans Vues qui affiche du texte et récupère la réponse
        # de l'utilisateur pour demander à l'organisateur le prénom du joueur
        surname = self.view.deal_with_input("Entrez le prénom du joueur {}: ".format(i))
        # 2 : appeler la fonction view_deal_with_input dans Vues qui affiche du texte et récupère la réponse
        # de l'utilisateur pour demander à l'organisateur le nom du joueur
        family_name = self.view.deal_with_input(
            "Entrez le nom du joueur {}: ".format(i)
        )
        # 3 : créer une boucle true
        while True:
            try:
                # 1 : appeler la fonction view_deal_with_input dans Vues qui affiche du texte et récupère la réponse
                # de l'utilisateur pour demander à l'organisateur la date de naissance du joueur
                date = self.view.deal_with_input(
                    "Entrez la date de naissance du joueur {} au format dd/mm/yyyy:".format(
                        i
                    )
                )
                # 2 : vérifier le format de l'input
                dte = datetime.strptime(date, "%d/%m/%Y")
                date_of_birth = dte
                # 3 : arrêter la boucle si le format est bon
                break
            # 2 : appeler la fonction view_deal_with_print dans Vues pour afficher la date entrée et notifier
            # à l'organisateur qu'il a entré un format invalide puis recommencer la boucle tant que
            # la date est incorrecte
            except ValueError as e:
                self.view.deal_with_print(e)
                self.view.deal_with_print("Format invalide")
        # 4 : appeler la fonction view_deal_with_input dans Vues qui affiche du texte et récupère la réponse
        # de l'utilisateur pour demander à l'organisateur le sexe du joueur
        sex = self.view.deal_with_input(
            "Entrez le sexe du joueur {} sous le format f ou m : ".format(i)
        )
        # 5 : créer une boucle while
        while sex != "m" and sex != "f":
            # 1 : appeler la fonction view_deal_with_input dans Vues qui affiche du texte et récupère la réponse
            # de l'utilisateur pour notifier l'organisateur tant que sa réponse est incorrecte et récupérer la bonne
            # réponse
            sex = self.view.deal_with_input(
                "Format invalide, veuillez rééssayer en entrant m ou f"
            )
        # 6 : appeler la fonction view_deal_with_input dans Vues qui affiche du texte et récupère la réponse
        # de l'utilisateur pour demander à l'organisateur le rang du joueur
        ranking = int(
            self.view.deal_with_input(
                "Entrez le rang du joueur {} en choisissant un chiffre entre 1 et 8: ".format(
                    i
                )
            )
        )
        # 7 : créer une boucle while pour vérifier si le rang du joueur est le même que celui d'un autre joueur
        while ranking in rankings_players:
            # 1 : appeler la fonction view_deal_with_input dans Vues qui affiche du texte et récupère la réponse
            # de l'utilisateur pour pour notifier l'organisateur tant que sa réponse est incorrecte et récupérer
            # la bonne réponse
            ranking = int(
                self.view.deal_with_input(
                    "Veuillez entrer un nombre différent de ceux déja entrés pour les autres joueurs {}:".format(
                        rankings_players
                    )
                )
            )
        # 8 : initialiser le score du joueur à 0
        score = 0
        # 9 : récupérer toutes les données du joueurs
        return surname, family_name, date_of_birth, sex, ranking, score

    # 10 : définir une fonction qui permet de sauvegarder les informations des joueurs
    def save_players(self, list_of_players):
        # 1 : appeler la fonction display_players dans Vues qui permet d'afficher les joueurs
        self.view.display_players(list_of_players)
        # 2 : appeler la fonction view_deal_with_input dans Vues qui affiche du texte et récupère la réponse
        # de l'utilisateur pour savoir s'il veut sauvegarder les joueurs
        answer = self.view.deal_with_input("Voulez-vous les sauvegarder ? y/n ?")
        # 3 : réinitialiser une liste des rangs des joueurs
        rankings_players = []
        # 4 : créer une boucle pour récupérer le rang de chaque joueur et l'ajouter à ranking_players
        for elem in list_of_players:
            rankings_players.append(elem.get_ranking())
        # 5 : si la réponse de l'utilisateur est oui
        if answer == "y":
            # 1 : appeler la fonction save_players dans models pour saugarder les joueurs
            self.models_player_db.save_players(list_of_players)
        # 6 : si la réponse de l'utilisateur est non
        elif answer == "n":
            # 2 : appeler la fonction view_deal_with_input dans Vues qui affiche du texte et récupère la réponse
            # de l'utilisateur pour savoir quel joueur il veut modifier
            number = self.view.deal_with_input(
                f"Quel joueur voulez-vous modifier? Entrez un numéro entre 1 et {len(list_of_players)}"
            )
            # 3 : créer une boucle while pour vérifier si le numéro du joueur à modifier n'est pas supérieur au
            # nombre de joueurs
            while not self.numberisvalid(number, len(list_of_players)):
                # 1 : appeler la fonction view_deal_with_input dans Vues qui affiche du texte et récupère la réponse
                # de l'utilisateur pour notifier l'utilisateur tant que sa réponse est incorrecte
                number = self.view.deal_with_input(
                    f"Veuillez entrer un numéro entre 1 et {len(list_of_players)}"
                )
            # 4 : transformer la réponse de l'utilisateur en entier
            number = int(number)
            # 5 : aller chercher le joueur concerné dans la liste des joueurs
            player = list_of_players[number - 1]
            # 6 : effacer le ranking précédent du joueur de la liste des rankings
            rankings_players.remove(player.get_ranking())
            # 7 : récupérer les informations du joueur avec la fonction get_info_of_player
            (
                surname,
                family_name,
                date_of_birth,
                sex,
                ranking,
                score,
            ) = self.get_info_of_player(rankings_players, number)
            # 8 : ajouter chaque information récupérée au joueur
            player.set_surname(surname)
            player.set_family_name(family_name)
            player.set_date_of_birth(date_of_birth)
            player.set_sex(sex)
            player.set_ranking(ranking)
            # 9 : revenir au début de la fonction pour sauvegarder ou modifier cette nouvelle liste
            return self.save_players(list_of_players)
        # 7 : si sa réponse est incorrecte
        else:
            # 1 : appeler la fonction view_deal_with_input dans Vues qui affiche du texte et récupère la réponse
            # de l'utilisateur pour notifier l'utilisateur tant que sa réponse est incorrecte
            self.view.deal_with_print("Veuillez entrer une réponse valide, y ou n")
            # 2 : revenir au début de la fonction
            self.save_players(list_of_players)
