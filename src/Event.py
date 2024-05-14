class Event:
    def __init__(self, t, func):
        self.t = t  # temps de l'événement
        self.func = func  # fonction à exécuter

    # comparaison pour la file d'attente prioritaire
    def __lt__(self, other):
        return self.t < other.t
