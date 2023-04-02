# coding : utf-8
from math import floor


class Grid:
    CELL_COLORED = 1
    CELL_NOT_COLORED = 0
    MIN_SIZE = 2

    def __init__(self, n: int, k: int):
        if not (isinstance(n, int) and isinstance(k, int)):
            raise TypeError("Les paramètres doivent être des entiers")
        if n < Grid.MIN_SIZE:
            raise AssertionError("La taille de la grille doit être de 2 ou plus")
        if k < 1 or k > floor((n * n) / 2):
            raise AssertionError("Le nombre de zone doit être compris entre [1; inf(n²/2)]")
        self.n = n  # taille de la grille
        self.k = k  # nombre de zones

        # tableau d'indice [i][j] correspondant aux coordonnées de la case avec sa valeur (1 coloriée, 0 sinon)
        self.cells = [[Grid.CELL_NOT_COLORED for _ in range(self.n)] for _ in range(self.n)]

    def getCellValue(self, i: int, j: int):
        if not (isinstance(i, int) and isinstance(j, int)):
            raise TypeError("Les coordonnées d'une case doivent être des entiers")
        if i > self.n or i < Grid.MIN_SIZE or j > self.n or j < Grid.MIN_SIZE:
            raise AssertionError("Les coordonnées ne sont pas dans la grille")
        return self.cells[i][j]

    def getGrid(self):
        return self.cells
