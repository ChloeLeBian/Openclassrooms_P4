from .globals import LIST_OF_MATCHES, NUMBER_OF_PLAYERS, NUMBER_MAX_OF_ROUNDS
from models import Round



class ControllerRounds:

    # 1 : ouvrir la liste des matchs
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

    # 7 : définir une fonction détaillant ce qui se passe quand on choisi 2 dans le menu
    # Rounds
    def step_two(self, x, nb_of_players, nb_of_rounds, matches, list_of_players, list_of_pairs_of_players):
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
            actual_round = (number_of_matches // (len(list_of_players) / 2) + 1)
            # 8 : si on est au premier round
            if actual_round == 1:
                # 1 : afficher le round actuel à l'organisateur
                self.view.deal_with_print("Vous êtes au round 1")
                # 2 : créer les premiers matchs
                first_matches = self.create_matches(
                    list_of_players, list_of_matches, 1
                )
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
                return self.menu(
                    list_of_players, list_of_pairs_of_players
                )
            # 9 : si on a dépassé le premier round mais que les limites de rounds maximum définies par l'oganisateur
            # et par le nombre de joueurs ne sont pas atteintes
            elif actual_round <= number_max_of_rounds and actual_round <= nb_of_rounds:
                # 1 : appeler la fonction view_deal_with_print dans Vues pour notifier à l'organisateur
                # le round auquel il est arrivé
                self.view.deal_with_print(
                    "Vous êtes au round {}".format(actual_round)
                )
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
                return self.menu(
                    list_of_players, list_of_pairs_of_players
                )
            # 10 : si le nombre de rounds défini par l'organisteur est atteint
            elif actual_round > number_max_of_rounds:
                # 1 : appeler la fonction view_deal_with_print dans Vues pour notifier à l'organisateur qu'il a
                # atteint le nombre de rounds maximum qu'il avait défini
                self.view.deal_with_print(
                    "Le nombre maximum de rounds choisis par l'oganisateur est atteint"
                )
                # 2 : revenir au menu
                return self.menu(
                    list_of_players, list_of_pairs_of_players
                )
            # 11 : si le nombre de rounds maximum possible est atteint
            elif actual_round > nb_of_rounds:
                # 1 : appeler la fonction view_deal_with_print dans Vues pour notifier à l'organisateur qu'il a
                # atteint le nombre de rounds maximum défini à partir du nombre de joueurs
                self.view.deal_with_print(
                    "Le nombre maximum de rounds possibles est atteint"
                )
                # 2 : revenir au menu
                return self.menu(
                    list_of_players, list_of_pairs_of_players
                )

    # 12 : définir une fonction qui permet de créer les rounds
    # Rounds
    def create_rounds(self, list_of_matches):
        # 1 : associer une liste de matchs à chaque round
        round = Round(name="Round", matches=list_of_matches)
        # 2 : récupérer le round
        return round

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
                score_1 = self.view.deal_with_input("Entrez le score de {} : ".format(j1))
                # 2 : créer une boucle while pour être sûr que le score est un float
                while not self.isfloat(score_1):
                    score_1 = self.view.deal_with_input("Entrez le score de {} (0, 1 ou 0.5) : ".format(j1))
                score_1 = float(score_1)
                # 3 : appeler la fonction view_deal_with_input dans Vues qui affiche du texte et récupère la réponse
                # de l'utilisateur pour obtenir le score du deuxième joueur
                score_2 = self.view.deal_with_input("Entrez le score de {} : ".format(j2))
                # 4 : créer une boucle while pour être sûr que le score est un float
                while not self.isfloat(score_2):
                    score_2 = self.view.deal_with_input("Entrez le score de {} (0, 1 ou 0.5) : ".format(j2))
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
            self.models_player_db.update_score_player(player, players, current_score_P1, j1)
            # 11 : appeler la fonction search_player de Models pour aller chercher le joueur 2 dans TinyDB
            current_player = self.models_player_db.search_player(player, players, j2)
            # 12 : ajouter le score que le joueur 2 a obtenu lors de son match à son ancien score
            current_score_P2 = float(current_player[0]["score"]) + score_2
            # 13 : appeler la fonction update_score_player dans Models pour modifier le score du joueur 2
            self.models_player_db.update_score_player(player, players, current_score_P2, j2)