from .globals import LIST_OF_MATCHES, NUMBER_OF_PLAYERS, NUMBER_MAX_OF_ROUNDS
from itertools import combinations
from models import Match


class ControllerMatches:

    # 1 : récupérer le nombre de joueurs
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
    
    # 4 : créer une fonction pour créer les matchs
    def create_matches(self, list_of_players, list_of_matches, round):
        # 1 : initialiser une liste de matchs possibles vide
        possible_matches = []
        # 2 : appeler la fonction get_players dans Models qui permet de récupérer les joueurs dans TinyDB
        players = self.models_player_db.get_players()
        players = players.all()
        # 3 : appeler la fonction get_matches dans Models qui permet de récupérer les matchs dans TinyDB
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
        # 5 : créer une fonction qui vérifie si pour deux matchs donnés un joueur ne joue pas deux fois en utilisant son prénom
        def possible_to_play(m,cm):
            for item in cm:
                if m[0]['surname'] == item[0]['surname'] or m[1]['surname'] == item[0]['surname']:
                    return False
                if m[0]["surname"] == item[1]["surname"] or m[1]["surname"] == item[1]["surname"]:
                    return False
            return True

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
                self.models_match_db.save_match(match.pair_of_players, match.score)
            # 3 : sauvegarder tous les matchs créés dans une liste
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
            # note: les matchs des joueurs les plus proches en terme de score sont prioritaires, il n'y a pas de doublon
            new_matches = list(combinations(players, 2))
            # 3 : obtenir une liste des matchs smplifiée, qui ne contient que le nom et le prénom des joueurs
            list_of_matches = [
                (x["pair_of_players"][0], x["pair_of_players"][1])
                for x in matches.all()
            ]
            # 4 : regarder pour tous les matchs possibles s'ils ont déjà été joués en regardant le prénom des joueurs
            # et ajouter les matchs non joués à la liste des matchs potentiels
            for m in new_matches:
                found = False
                for j in list_of_matches:
                    if found or match_eq(m, j):
                        found = True
                if not found:
                    possible_matches.append(m)
            # 5 : créer une liste de matchs à garder
            current_matches = []
            # 6 : vérifier pour chaque si un joueur ne joue pas deux fois en le comparant aux éléments des matchs du round
            # dans current_matches grâce à la fonction possible_to_play
            for m in possible_matches:
                if possible_to_play(m,current_matches):
                    current_matches.append(m)       
            # 7 : obtenir la liste des matchs sans les nouveaux matchs potentiels
            list_of_matches = [
                Match(x["pair_of_players"], x["score"]) for x in matches.all()
            ]
            # 8 : créer des tuples à partir des nouveaux matchs potentiels et les sauvegarder
            current_matches = [Match((x, y)) for x, y in current_matches]
            for m in current_matches:
                self.models_match_db.save_match(m.pair_of_players, m.score)
            # 9 : ajouter ces nouveaux matchs à la liste des matchs
            list_of_matches += current_matches
            # 10 : récupérer la liste des matchs complétée et les nouveaux matchs
            return list_of_matches, current_matches
    
            
            