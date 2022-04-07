from itertools import combinations
from models import Match, MatchDB, Player, PlayerDB, Round
from vues import Vues
from datetime import datetime


class Controller:

    # 1 : ouvrir la liste des matchs
    global list_of_matches
    list_of_matches = []

    # 2 : définir le nombre de joueurs
    global number_of_players
    number_of_players = 8

    # 3 : définir le nombre maximum de rounds
    global number_max_of_rounds
    number_max_of_rounds = 4

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

    # 6 : définir une fonction détaillant ce qui se passe quand on choisi 1 dans le menu
    # Players
    def step_one(self, x, list_of_players, list_of_pairs_of_players):
        # 1 : si la liste des joueurs dans Tinydb est vide
        if x == 0:
            # 1 : appeler la fonction create_players pour créer les joueurs
            list_of_players = self.create_players(number_of_players)
            # 2 : appeler la fonction save_players pour sauvegarder les joueurs
            self.save_players(list_of_players)
            # 3 : retourner le menu
            return self.menu(list_of_players, list_of_pairs_of_players)

        # 2 : si la liste des joueurs dans Tinydb n'est pas vide
        else:
            # 1 : appeler la fonction view_deal_with_print dans Vues pour notifier à l'organisateur
            # qu'il a déjà enregistré ses joueurs
            self.view.deal_with_print(
                "Vous avez déjà enregistrés vos joueurs, veuillez générer vos rounds\n\r"
            )
            # 2 : retourner le menu
            return self.menu(list_of_players, list_of_pairs_of_players)

    # 7 : définir une fonction détaillant ce qui se passe quand on choisi 2 dans le menu
    # Rounds
    def step_two(
        self,
        x,
        nb_of_players,
        nb_of_rounds,
        matches,
        list_of_players,
        list_of_pairs_of_players,
    ):
        # 1 : si la liste des joueurs dans Tinydb est vide
        if x == 0:
            # 1 : appeler la fonction view_deal_with_print dans Vues pour notifier à l'organisateur
            # qu'il doit enregistrer ses joueurs
            self.view.deal_with_print(
                "Veuillez rentrer vos joueurs avant de générer un round\n\r"
            )
            # 2 : appeler la fonction create_players pour créer les joueurs
            list_of_players = self.create_players(number_of_players)
            # 3 : appeler la fonction save_players pour sauvegarder les joueurs
            self.save_players(list_of_players)
            # 4 : retourner le menu
            return self.menu(list_of_players, list_of_pairs_of_players)
        # 2 : si la liste des joueurs dans Tinydb n'est pas vide
        else:
            # 3 : afficher le nombre de rounds possible
            self.view.deal_with_print(
                "Nombre de rounds possible {}\n\r".format(nb_of_rounds)
            )
            # 4 : afficher le nombre de rounds maximum défini par l'organisateur
            self.view.deal_with_print(
                "Nombre de rounds maximum défini {}\n\r".format(number_max_of_rounds)
            )
            # 5 : afficher le nombre de joueurs
            self.view.deal_with_print(
                "voici le nombre de joueurs {}\n\r".format(nb_of_players)
            )
            # 6 : calculer le nombre de matchs déjà joués à partir de la liste des matchs
            # extraite de Tinydb au préalable
            number_of_matches = len(matches.all())
            # 7 : calculer le round actuel en fonction du nombre de matchs déjà joués
            actual_round = number_of_matches // (len(list_of_players) / 2) + 1
            # 8 : si on est au premier round
            if actual_round == 1:
                # 1 : afficher le round actuel à l'organisateur
                self.view.deal_with_print("Vous êtes au round 1")
                # 2 : créer les premiers matchs
                first_matches = self.create_matches(list_of_players, list_of_matches, 1)
                # 3 : appeler la fonction display matches dans Vues pour afficher les matchs créés
                self.view.display_matches(first_matches, match_to_display=1)
                # 4 : créer le round à partir des matchs
                first_round = self.create_rounds(first_matches)
                # 5 : créer la liste des paires de joueurs
                list_of_pairs_of_players = self.create_list_of_pairs_of_players(
                    first_matches, list_of_pairs_of_players
                )
                # 6 : appeler la fonction set_score pour ajouter un score aux matchs
                self.set_score(first_round)
                # 7 : revenir au menu
                return self.menu(list_of_players, list_of_pairs_of_players)
            # 9 : si on a dépassé le premier round mais que les limites de rounds maximum définies par l'oganisateur
            # et par le nombre de joueurs ne sont pas atteintes
            elif actual_round <= number_max_of_rounds and actual_round <= nb_of_rounds:
                # 1 : appeler la fonction view_deal_with_print dans Vues pour notifier à l'organisateur
                # le round auquel il est arrivé
                self.view.deal_with_print("Vous êtes au round {}".format(actual_round))
                # 2 : créer les matchs
                match, current_match = self.create_matches(
                    list_of_players, list_of_matches, actual_round
                )
                # 3 : ouvrir une liste pour suivre le décompte des matchs
                match_to_display = []
                # 4 : définir l'index à partir duquel on va choisir les matchs à afficher
                start_display_range = match.index(current_match[0])
                # 5 : définir le rang dans lequel seront compris les matchs à afficher
                # et les ajouter à la liste display_matches pour suivre le décompte des matchs
                for n in range(
                    start_display_range,
                    int(start_display_range + len(list_of_players) / 2),
                ):
                    match_to_display.append(match[n])
                # 6 : apeler la fonction display_matches Vues pour afficher les matchs choisis
                self.view.display_matches(
                    match_to_display, match_to_display=start_display_range + 1
                )
                # 7 : créer le round à partir des matchs
                round = self.create_rounds(current_match)
                # 8 : ajouter les paires de joueurs des matchs à la liste des paires de joueurs
                list_of_pairs_of_players = self.create_list_of_pairs_of_players(
                    match, list_of_pairs_of_players
                )
                # 8 : appeler la fonction set_score pour ajouter un score aux matchs
                self.set_score(round)
                # 9 : revenir au menu
                return self.menu(list_of_players, list_of_pairs_of_players)
            # 10 : si le nombre de rounds défini par l'organisteur est atteint
            elif actual_round > number_max_of_rounds:
                # 1 : appeler la fonction view_deal_with_print dans Vues pour notifier à l'organisateur qu'il a
                # atteint le nombre de rounds maximum qu'il avait défini
                self.view.deal_with_print(
                    "Le nombre maximum de rounds choisis par l'oganisateur est atteint"
                )
                # 2 : revenir au menu
                return self.menu(list_of_players, list_of_pairs_of_players)
            # 11 : si le nombre de rounds maximum possible est atteint
            elif actual_round > nb_of_rounds:
                # 1 : appeler la fonction view_deal_with_print dans Vues pour notifier à l'organisateur qu'il a
                # atteint le nombre de rounds maximum défini à partir du nombre de joueurs
                self.view.deal_with_print(
                    "Le nombre maximum de rounds possibles est atteint"
                )
                # 2 : revenir au menu
                return self.menu(list_of_players, list_of_pairs_of_players)

    # 8 : définir une fonction qui permet de classer les joueurs selon leur score par ordre décroissant
    # Players
    def rank_players(self):
        # 1 : appeler la fonction get_players dans Mo3dels qui permet de récupérer les joueurs dans TinyDB
        # et les mettre dans une liste de joueurs
        list_of_players = self.models_player_db.get_players()
        # 2 : classer les joueurs de la liste selon leur score
        list_of_players = sorted(
            list_of_players, key=lambda d: d["score"], reverse=True
        )
        # 3 : appeler la fonction display ranking dans Vues qui permet d'afficher
        # les joueurs, leur score et leur rang
        self.view.display_ranking(list_of_players)

    # 8 : définir une fonction qui permet de créer des joueurs en fonction du
    # nombre de joueurs défini
    # Players
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
    # Players
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
    # Players
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

    # 11 : définir une fonction qui permet de créer les matchs
    # Matches
    def create_matches(self, list_of_players, list_of_matches, round):
        # 1 : initialiser une liste de matchs vide
        current_match = []
        # 2 : appeler la fonction get_players dans Models qui permet de récupérer les joueurs dans TinyDB
        players = self.models_player_db.get_players()
        players = players.all()
        # 3 : appeler la fonction get_matches dans Models qui permet de récupérer les joueurs dans TinyDB
        matches = self.models_match_db.get_matches()
        # 4 : vérifier toutes les combinaisons de matchs dans lesquels deux joueurs ont le même nom
        # de famille
        match_eq = lambda x, y: (
            (x[0]["surname"] == y[0]["surname"] and x[1]["surname"] == y[1]["surname"])
            or (
                x[1]["surname"] == y[0]["surname"]
                and x[0]["surname"] == y[1]["surname"]
            )
        )
        # 5 : vérifier toutes les combinaisons de joueurs qui ont le même nom de famille
        player_in = lambda x, y: (
            (x["surname"] == y[0]["surname"]) or (x["surname"] == y[1]["surname"])
        )
        # 6 : si on est au round 1
        if round == 1:
            # 1 : classer les joueurs par rang et par ordre croissant
            players = sorted(players, key=lambda i: i["ranking"])
            # 2 : créer une boucle pour tous les joueurs allant de 1 à la moitié de la liste
            for i in range(0, int(len(list_of_players) / 2)):
                # 1 : associer le joueur le joueur au joueur qui lui est opposé à partir de la
                # moitié de la liste (ex : joueur 1 et joueur 5 si huit joueur, joueur 1 et joueur 6 si 10 joueurs)
                match = Match((players[i], players[i + int(len(list_of_players) / 2)]))
                # 2 : appeler la fonction save_match dans Models pour sauvegarder le match
                match.save_match()
            # 3 : sauvegarder tous les matchs crées dans une liste
            list_of_matches = [
                Match(x["pair_of_players"], x["score"]) for x in matches.all()
            ]
            # 4 récupérer la liste des matchs créés
            return list_of_matches
        # 7 : si on est à un round supérieur à 1
        else:
            # 1 : classer les joueurs en fonction de leur score dans l'ordre décroissant
            players = sorted(players, key=lambda i: i["score"], reverse=True)
            # 2 : utiliser itertools de python pour obtenir toutes les combinaisons de matchs possibles
            # note: les matchs des joueurs les plus proches en terme de score sont prioritaires
            new_matches = list(combinations(players, 2))
            # 3 : obtenir une liste des matchs smplifiée, qui ne contient que le nom et le prénom des joueurs
            list_of_matches = [
                (x["pair_of_players"][0], x["pair_of_players"][1])
                for x in matches.all()
            ]
            # 4 : regarder pour tous les matchs possibles s'ils ont déjà été joués en regardant le nom des joueurs
            # et ajouter les matchs non joués à la liste des matchs potentiels
            for m in new_matches:
                found = False
                for j in list_of_matches:
                    if found or match_eq(m, j):
                        found = True
                if not found:
                    current_match.append(m)
            # 5 : créer une liste de matchs à effacer
            to_delete = []
            # 6 : vérifier tous les matchs dans lesquels un joueur se trouve à nouveau
            # afin qu'il ne joue pas deux fois et les ajouter aux matchs à effacer
            for i in range(len(current_match)):
                temp = current_match[i]
                check_matches = [
                    x for x in current_match[i + 1 :] if x not in to_delete
                ]
                for m in check_matches:
                    if player_in(temp[0], m) or player_in(temp[1], m):
                        if len(current_match) - len(to_delete) > len(players) / 2:
                            to_delete.append(m)
            # 7 : effacer tous les matchs à effacer de la liste des matchs potentiels
            for m in to_delete:
                current_match.remove(m)
            # 8 : obtenir la liste des matchs sans les nouveaux matchs potentiels
            list_of_matches = [
                Match(x["pair_of_players"], x["score"]) for x in matches.all()
            ]
            # 9 : créer des tuples à partir des nouveaux matchs potentiels et les sauvegarder
            current_match = [Match((x, y)) for x, y in current_match]
            for m in current_match:
                m.save_match()
            # 10 : ajouter ces nouveaux matchs à la liste des matchs
            list_of_matches += current_match
            # 11 : récupérer la liste des matchs complétée et les nouveaux matchs
            return list_of_matches, current_match

    # 12 : définir une fonction qui permet de créer les rounds
    # Rounds
    def create_rounds(self, list_of_matches):
        # 1 : associer une liste de matchs à chaque round
        round = Round(name="Round", matches=list_of_matches)
        # 2 : récupérer le round
        return round

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

    # 14 : définir une fonction qui permet de rentrer les scores des joueurs pour chaque round
    # Rounds ou Players?
    def set_score(self, round):
        # 1 : créer une boucle pour tous les matchs du round
        for elem in round.matches:
            # 1 : récupérer grâce à la fonction get_pair_of_players les joueurs
            # de chaque match
            pair_of_players = elem.get_pair_of_players()
            # 2 : récupérer le nom de famille de chaque joueur
            j1 = pair_of_players[0]["family_name"]
            j2 = pair_of_players[1]["family_name"]
            # 3 : créer une boucle while qui permet de vérifier les scores entrés pour chaque match
            repeat = True
            while repeat:
                # 1 : appeler la fonction view_deal_with_input dans Vues qui affiche du texte et récupère la réponse
                # de l'utilisateur pour obtenir le score du premier joueur
                score_1 = self.view.deal_with_input(
                    "Entrez le score de {} : ".format(j1)
                )
                # 2 : créer une boucle while pour être sûr que le score est un float
                while not self.isfloat(score_1):
                    score_1 = self.view.deal_with_input(
                        "Entrez le score de {} (0, 1 ou 0.5) : ".format(j1)
                    )
                score_1 = float(score_1)
                # 3 : appeler la fonction view_deal_with_input dans Vues qui affiche du texte et récupère la réponse
                # de l'utilisateur pour obtenir le score du deuxième joueur
                score_2 = self.view.deal_with_input(
                    "Entrez le score de {} : ".format(j2)
                )
                # 4 : créer une boucle while pour être sûr que le score est un float
                while not self.isfloat(score_2):
                    score_2 = self.view.deal_with_input(
                        "Entrez le score de {} (0, 1 ou 0.5) : ".format(j2)
                    )
                score_2 = float(score_2)
                # 5 : vérifier si les deux scores additionés ne font pas 1
                if score_1 + score_2 != 1.0:
                    # 1 : appeler la fonction view_deal_with_input dans Vues qui affiche du texte et récupère la réponse
                    # de l'utilisateur pour notifier l'organisateur que les scores entrés ne sont pas corrects
                    self.view.deal_with_print(
                        "Veuillez entrer les bons scores (0, 1, 0.5)"
                    )
                # 6 : arrêter la boucle si les deux scores additionés font 1
                else:
                    repeat = False
            # 2 : appeler la fonction set_score dans Models pour récupérer les deux scores
            elem.set_score([score_1, score_2])
            # 3 : appeler la fonction get_players de Models pour récupérer les joueurs dans TinyDB
            players = self.models_player_db.get_players()
            # 4 : appeler la fonction get_matches de Models pour récupérer les joueurs dans TinyDB
            matches = self.models_match_db.get_matches()
            # 5 : appeler la fonction query_player de Models pour aller chercher les informations
            #  des joueurs dans TinyDB
            player = self.models_player_db.query_player()
            # 6 : appeler la fonction query_match de Models pour aller chercher les informations
            #  des matchs dans TinyDB
            match = self.models_match_db.query_match()
            # 7 : appeler la fonction initiate_score de Models pour initialiser le score du match dans TinyDB
            self.models_match_db.initiate_score__matches(matches, match, elem)
            # 8 : appeler la fonction search_player de Models pour aller chercher le joueur 1 dans TinyDB
            current_player = self.models_player_db.search_player(player, players, j1)
            # 9 : ajouter le score que le joueur 1 a obtenu lors de son match à son ancien score
            current_score_P1 = float(current_player[0]["score"]) + score_1
            # 10 : appeler la fonction update_score_player dans Models pour modifier le score du joueur 1
            self.models_player_db.update_score_player(
                player, players, current_score_P1, j1
            )
            # 11 : appeler la fonction search_player de Models pour aller chercher le joueur 2 dans TinyDB
            current_player = self.models_player_db.search_player(player, players, j2)
            # 12 : ajouter le score que le joueur 2 a obtenu lors de son match à son ancien score
            current_score_P2 = float(current_player[0]["score"]) + score_2
            # 13 : appeler la fonction update_score_player dans Models pour modifier le score du joueur 2
            self.models_player_db.update_score_player(
                player, players, current_score_P2, j2
            )

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


if __name__ == "__main__":
    controller = Controller()
    controller.menu()
