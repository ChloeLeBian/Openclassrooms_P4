from models import matches


class Vues:
    # 1 : initialiser PlayerDB
    def __init__(self):
        pass

    # 2 : définir une fonction qui permet d'afficher les matchs
    def display_matches(self, match, match_to_display):
        # 1 : créer une boucle pour tous aller chercher les joueurs du matchs
        for i in range(0, int(len(match))):
            # 1 : récupérer la paire de joueurs du match
            pair_of_players = match[i].get_pair_of_players()
            # 2 : récupérer le nom de famille et le prénom du joueur 1
            output_1 = f"{pair_of_players[0]['surname']} {pair_of_players[0]['family_name']}"
            # 3 : récupérer le nom de famille et le prénom du joueur 2
            output_2 = f"{pair_of_players[1]['surname']} {pair_of_players[1]['family_name']}"
            # 4 : afficher le match
            print(f"Match {output_1} VS {output_2}")

    # 3 : définir une fonction qui permet d'afficher les joueurs
    def display_players(self, list_of_players):
        players = list_of_players
        # 1 : créer une boucle pour chaque joueur
        for player in players:
            # 1 : afficher ses informations
            print(
                player.family_name,
                player.surname,
                player.sex,
                player.date_of_birth,
                player.ranking,
            )

    # 4 : définir une fonction qui permet d'afficher le rang des joueurs dans le classement
    def display_ranking(self, list_of_players):
        # 1 : initialiser le rang à 1
        ranking = 1
        # 2 : créer une boucle pour chaque joueur
        for player in list_of_players:
            # 1 : afficher son rang, son nom et son score total
            print(
                f"{ranking} - {player['family_name']} {player['surname']} - {player['score']}"
            )
            # 2 : ajouter 1 à chaque nouveau passage de la boucle
            ranking = ranking + 1

    # 5 : définir une fonction qui permet d'afficher tous les matchs d'un tournoi
    def display_match_tournament(self, list_of_matches):
        # 1 : définir une variable i qui va indiquer l'index de chaque match
        i = 1
        # 2 : créer une boucle pour chaque match de la liste
        for match in list_of_matches:
            # 1 : récupérer la paire de joueurs de chaque match
            pair_of_players = match['pair_of_players']
            # 2 : récupérer le score de chaque match
            score = match['score']
            # 3 : récupérer le nom de chaque joueur et le score
            output_1 = f"{pair_of_players[0]['surname']} {pair_of_players[0]['family_name']}"
            output_2 = f"{pair_of_players[1]['surname']} {pair_of_players[1]['family_name']}"
            output_3 = f"{score}"
            # 4 : afficher ces informations à l'utilisateur
            print(f"Match {i} : {output_1} VS {output_2}:{output_3}")
            i = i + 1

    # 6 : définir une fonction qui permet d'afficher un message et de récupérer la reponse de l'utilisateur
    def deal_with_input(self, message):
        return input(message)

    # 7 : définir une fonction qui permet d'afficher un message
    def deal_with_print(self, message):
        return print(message)
