# coding : utf-8

from math import floor


class Grid:
    CELL_COLORED = 1
    CELL_NOT_COLORED = 0
    GRID_MIN_SIZE = 2
    GRID_MIN_INDEX = 0
    ZONE_MIN_NUMBER = 1

    def __init__(self, n: int, zone: int):
        """
        Vérifie les paramètres et initialise toutes les variables
        :param n: taille de la grille (n*n)
        :type n: int
        :param zone: nombre de zones dans la grille
        :type zone: int
        """
        if not (isinstance(n, int) and isinstance(zone, int)):
            raise TypeError("Les paramètres doivent être des entiers")
        if n < Grid.GRID_MIN_SIZE:
            raise AssertionError("La taille de la grille doit être de 2 ou plus")
        if zone < 1 or zone > floor((n * n) / 2):
            raise AssertionError("Le nombre de zone doit être compris entre [1; inf(n²/2)]")
        self.n = n  # taille de la grille
        self.zone = zone  # nombre de zones
        self.coloredCells = 0  # nombre de cases coloriées dans la configuration initiale

        # tableau d'indice [i][j] correspondant aux coordonnées de la case (i+1, j+1) avec les valeurs : [(1 coloriée, 0 sinon), zone de la case, id]
        self.cells = []
        self.__generateCells()

    def __generateCells(self):
        """
        Génère le tableau contenant les données de chaque case
        """
        idCell = 1
        for i in range(self.n):
            subs = []
            for j in range(self.n):
                subs.append([Grid.CELL_NOT_COLORED, 1, idCell])
                idCell += 1
            self.cells.append(subs)

    def getIdCell(self, i: int, j: int):
        """
        Renvoie l'identifiant d'une case à partir de ses coordonnées
        :param i: première coordonnée
        :type i: int
        :param j: deuxième coordonnée
        :type j: int
        :return: identifiant
        :rtype: int
        """
        if not (isinstance(i, int) and isinstance(j, int)):
            raise TypeError("Les coordonnées d'une case doivent être des entiers")
        if i > self.n or i <= Grid.GRID_MIN_INDEX or j > self.n or j <= Grid.GRID_MIN_INDEX:
            raise AssertionError("Les coordonnées ne sont pas dans la grille")
        return self.cells[i - 1][j - 1][2]

    def getCellIJById(self, idCell: int):
        """
        Renvoie les coordonnées d'une case à partir de son identifiant
        :param idCell: identifiant
        :type idCell: int
        :return: coordonnées
        :rtype: list
        """
        if not (isinstance(idCell, int)):
            raise TypeError("L'identifiant d'une case doit être un entier")
        if idCell > (self.n * self.n) or idCell <= 0:
            raise AssertionError("Mauvaise valeur de l'identifiant")
        for i in range(self.n):
            for j in range(self.n):
                if self.cells[i][j][2] == idCell:
                    return [i + 1, j + 1]
        raise ValueError(f"Aucune case ne possède l'identifiant {idCell}")

    def getGrid(self):
        """
        Renvoie le tableau contenant toutes les cases ainsi que les informations associées
        :return: les cases
        :rtype: list
        """
        return self.cells

    def getGridSize(self):
        """
        Renvoie la taille de la grille
        :return: taille
        :rtype: int
        """
        return self.n

    def getZoneNumber(self):
        """
        Renvoie le nombre de zone
        :return: nombre zone
        :rtype: int
        """
        return self.zone

    def getNumberColoredCells(self):
        """
        Renvoie le nombre de cases coloriées (aide pour le calcul duu nombre de variables dans les clauses)
        :return: nombre cases
        :rtype: int
        """
        return self.coloredCells

    def getCellsInZone(self, size: int, zone: int):
        """
        Renvoie les identifiants des cases dans la zone passée en paramètre
        :param size: taille de la grille
        :type size: int
        :param zone: numéro zone
        :type zone: int
        :return: cases dans zone
        :rtype: list
        """
        casesInZone = []
        for i in range(1, size + 1):
            for j in range(1, size + 1):
                if self.getCellValueZone(i, j) == zone:
                    casesInZone.append(self.getIdCell(i, j))
        return casesInZone

    def getCellValueZone(self, i: int, j: int):
        """
        Renvoie dans quelle zone est la cellule de coordonnées (i, j)
        :param i: première coordonnée
        :type i: int
        :param j: deuxième coordonnée
        :type j: int
        :return: numéro de la zone
        :rtype: int
        """
        if not (isinstance(i, int) and isinstance(j, int)):
            raise TypeError("Les coordonnées d'une case doivent être des entiers")
        if i > self.n or i <= Grid.GRID_MIN_INDEX or j > self.n or j <= Grid.GRID_MIN_INDEX:
            raise AssertionError("Les coordonnées ne sont pas dans la grille")
        return self.cells[i - 1][j - 1][1]

    def setCellValueZone(self, i: int, j: int, k: int):
        """
        Permet d'affecter une zone à une case
        :param i: première coordonnée
        :type i: int
        :param j: deuxième coordonnée
        :type j: int
        :param k: numéro de la zone à mettre à la celulle (i, j)
        :type k: int
        :return: Renvoie lui-même
        :rtype: Grid
        """
        if not (isinstance(i, int) and isinstance(j, int) and isinstance(k, int)):
            raise TypeError("Les coordonnées d'une case doivent être des entiers")
        if i > self.n or i <= Grid.GRID_MIN_INDEX or j > self.n or j <= Grid.GRID_MIN_INDEX or k > self.zone or k < Grid.ZONE_MIN_NUMBER:
            raise AssertionError("Les coordonnées ne sont pas dans la grille")
        self.cells[i - 1][j - 1][1] = k
        return self

    def getCellValueColor(self, i: int, j: int):
        """
        Permet de récupérer la couleur de la case (i, j) appartenant à la zone k
        :param i: première coordonnée
        :type i: int
        :param j: deuxième coordonnée
        :type j: int
        :param k: numéro de la zone à mettre à la celulle (i, j)
        :type k: int
        :return: couleur de la case
        :rtype: int
        """
        if not (isinstance(i, int) and isinstance(j, int)):
            raise TypeError("Les coordonnées d'une case doivent être des entiers")
        if i > self.n or i <= Grid.GRID_MIN_INDEX or j > self.n or j <= Grid.GRID_MIN_INDEX:
            raise AssertionError("Les coordonnées ne sont pas dans la grille")
        return self.cells[i - 1][j - 1][0]

    def setCellValueColor(self, i: int, j: int, color: int):
        """
        Permet d'affecter une couleur à la case (i, j)
        :param i: première coordonnée
        :type i: int
        :param j: deuxième coordonnée
        :type j: int
        :param color:
        :type color: int
        """
        if not (isinstance(i, int) and isinstance(j, int) and isinstance(color, int)):
            raise TypeError("Les paramètres pour définir une case coloriée doivent être des entiers")
        if i > self.n or i <= Grid.GRID_MIN_INDEX or j > self.n or j <= Grid.GRID_MIN_INDEX:
            raise AssertionError("Les coordonnées ne sont pas dans la grille")
        if color != Grid.CELL_COLORED and color != Grid.CELL_NOT_COLORED:
            raise ValueError("Le paramètre de la couleur doit valoir 0 (non coloriée) ou 1 (coloriée)")
        if color == Grid.CELL_COLORED:
            self.coloredCells += 1
        else:
            if self.coloredCells > 0:
                self.coloredCells -= 1
        self.cells[i - 1][j - 1][0] = color
