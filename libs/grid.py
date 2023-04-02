# coding : utf-8
from math import floor


class Grid:
    def __init__(self, n: int, k: int):
        if not (isinstance(n, int) and isinstance(k, int)):
            raise TypeError("Les paramètres doivent être des entiers")
        if n < 2:
            raise AssertionError("La taille de la grille doit être de 2 ou plus")
        if k < 1 or k > floor((n * n) / 2):
            raise AssertionError("Le nombre de zone doit être compris entre [1; inf(n²/2)]")
        self.n = n  # taille de la grille
        self.k = k  # nombre de zones
