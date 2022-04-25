from controllers import Controller
#from vues import Vues

# 1 : initialiser Controller et Vues
controller = Controller()
#vues = Vues()

# 2 : initaliser la liste des joueurs
list_of_players = []

# 3 : appeler le menu
controller.menu(list_of_players)
