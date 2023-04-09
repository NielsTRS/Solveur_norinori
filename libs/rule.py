# coding : utf-8

import itertools

import libs.grid as grid


class Rule:
    def __init__(self, gridLib: grid):
        """
        Initialise toutes les variables
        :param gridLib:
        :type gridLib:
        """
        if not isinstance(gridLib, grid.Grid):
            raise ImportError("L'instance passée en paramètre doit être de la classe : grid")
        self.clauses = []
        self.gridLib = gridLib
        self.n = gridLib.getGridSize()

    def __generateNeighborClauses(self):
        """
        Génère les clauses pour que les cases soient coloriés deux par deux
        """

        def addClause(x: int, y: int, positive: bool, *args: tuple):
            """
            Fonction intermédiaire permettant d'ajouter une clause
            :param x: première coordonnée
            :type x: int
            :param y: deuxième coordonnée
            :type y: int
            :param positive: permet de gérer si on met à la négation ou non
            :type positive: bool
            :param args: les autres arguments à ajouter de la même façon que x, y, positive
            :type args: tuple
            """
            tempClauses = []
            prefix = "" if positive else "-"
            tempClauses.append(int(f"{prefix}{self.gridLib.getIdCell(x, y)}"))
            for arg in args:
                prefix = "" if arg[2] else "-"
                tempClauses.append(int(f"{prefix}{self.gridLib.getIdCell(arg[0], arg[1])}"))
            self.clauses.append(tempClauses)

        for i in range(1, self.n + 1):
            for j in range(1, self.n + 1):
                if i == 1 and j == 1:  # case en haut a gauche x_{i-1,j} et x_{i,j-1} n'existent pas
                    addClause(i, j, False, (i, j + 1, True), (i + 1, j, True))
                    addClause(i, j, False, (i, j + 1, False), (i + 1, j, False))

                elif i == 1 and j == self.n:  # case en haut à droite x_{i-1,j} et x_{i,j+1} n'existent pas
                    addClause(i, j, False, (i, j - 1, True), (i + 1, j, True))
                    addClause(i, j, False, (i, j - 1, False), (i + 1, j, False))

                elif i == self.n and j == 1:  # case en bas a gauche x_{i+1,j} et x_{i,j-1} n'existent pas
                    addClause(i, j, False, (i, j + 1, True), (i - 1, j, True))
                    addClause(i, j, False, (i, j + 1, False), (i - 1, j, False))

                elif i == self.n and j == self.n:  # case en bas à droite x_{i+1,j} et x_{i,j+1} n'existent pas
                    addClause(i, j, False, (i, j - 1, True), (i - 1, j, True))
                    addClause(i, j, False, (i, j - 1, False), (i - 1, j, False))

                elif i == 1:  # cases sur la premiere ligne x_{i-1,j} n'existe pas
                    addClause(i, j, False, (i, j - 1, True), (i, j + 1, True), (i + 1, j, True))
                    addClause(i, j, False, (i, j - 1, False), (i, j + 1, False))
                    addClause(i, j, False, (i, j - 1, False), (i + 1, j, False))
                    addClause(i, j, False, (i, j + 1, False), (i + 1, j, False))

                elif i == self.n:  # cases sur la derniere ligne x_{i+1,j} n'existe pas
                    addClause(i, j, False, (i, j - 1, True), (i, j + 1, True), (i - 1, j, True))
                    addClause(i, j, False, (i, j - 1, False), (i, j + 1, False))
                    addClause(i, j, False, (i, j - 1, False), (i - 1, j, False))
                    addClause(i, j, False, (i, j + 1, False), (i - 1, j, False))

                elif j == 1:  # cases sur la premiere colonne x_{i, j_1} n'existe pas
                    addClause(i, j, False, (i + 1, j, True), (i, j + 1, True), (i - 1, j, True))
                    addClause(i, j, False, (i + 1, j, False), (i, j + 1, False))
                    addClause(i, j, False, (i + 1, j, False), (i - 1, j, False))
                    addClause(i, j, False, (i, j + 1, False), (i - 1, j, False))

                elif j == self.n:  # cases sur la dernière colonne x_{i, j+1} n'existe pas
                    addClause(i, j, False, (i + 1, j, True), (i, j - 1, True), (i - 1, j, True))
                    addClause(i, j, False, (i + 1, j, False), (i, j - 1, False))
                    addClause(i, j, False, (i + 1, j, False), (i - 1, j, False))
                    addClause(i, j, False, (i, j - 1, False), (i - 1, j, False))

                else:  # toutes les autres cases
                    addClause(i, j, False, (i - 1, j, False), (i, j - 1, False))
                    addClause(i, j, False, (i - 1, j, False), (i, j + 1, False))
                    addClause(i, j, False, (i - 1, j, False), (i + 1, j, False))
                    addClause(i, j, False, (i - 1, j, True), (i, j - 1, True), (i, j + 1, True), (i + 1, j, True))
                    addClause(i, j, False, (i, j - 1, False), (i, j + 1, False))
                    addClause(i, j, False, (i, j - 1, False), (i + 1, j, False))
                    addClause(i, j, False, (i, j + 1, False), (i + 1, j, False))

    def __generateZoneClauses(self):
        """
        Génère les clauses pour que chaque zone est strictement deux cases coloriées
        """
        gridSize = self.gridLib.getGridSize()
        gridZoneNumber = self.gridLib.getZoneNumber()
        for k in range(1, gridZoneNumber + 1):
            casesInZone = []
            for i in range(1, gridSize + 1):
                for j in range(1, gridSize + 1):
                    if self.gridLib.getCellValueZone(i, j) == k:
                        casesInZone.append(self.gridLib.getIdCell(i, j))
            n = len(casesInZone)
            combs = itertools.combinations(range(1, n + 1), n - 1)
            for comb in combs:
                temp = []
                for j in comb:
                    temp.append(casesInZone[j - 1])
                self.clauses.append(temp)

            combs = itertools.combinations(range(1, n + 1), 3)
            for comb in combs:
                temp = []
                for j in comb:
                    temp.append(-casesInZone[j - 1])
                self.clauses.append(temp)

    def __filterClauses(self):
        """
        Permet de supprimer les clauses ayant un élément "vrai" lorsqu'une case est mise comme coloriée lors de la configuration initiale
        """
        clauses = self.getClauses()
        filtered_clauses = []
        for clause in clauses:
            filtered_clause = []
            add_clause = True
            for id in clause:
                cell = self.gridLib.getCellIJById(abs(id))
                color = self.gridLib.getCellValueColor(cell[0], cell[1])
                if id > 0:
                    if color != self.gridLib.CELL_COLORED:
                        filtered_clause.append(id)
                    else:
                        add_clause = False
                        break  # on évite de boucler sur les autres terms alors qu'on ne pas garder la clause
                else:
                    if color != self.gridLib.CELL_COLORED:
                        filtered_clause.append(id)
            if add_clause:
                filtered_clauses.append(filtered_clause)

        self.clauses = filtered_clauses

    def __getNumberVar(self):
        """
        Renvoie le nombre d'identifiants différents dans les clauses
        :return: nombre identifiant
        :rtype: int
        """
        return self.n * self.n - self.gridLib.getNumberColoredCells()

    def __getNumberClauses(self):
        """
        Renvoie le nombre de clauses
        :return: nombre clauses
        :rtype: int
        """
        return len(self.getClauses())

    def getClauses(self):
        """
        Renvoie les clauses
        :return: clauses
        :rtype: list
        """
        return self.clauses

    def generateDimacs(self, filename: str):
        """
        Génère un fichier au format dimacs
        :param filename: nom du fichier
        :type filename: str
        """
        f = open(filename, "w")
        f.write(f"p cnf {self.__getNumberVar()} {self.__getNumberClauses()} \n")
        text = ""
        for clause in self.getClauses():
            for name in clause:
                text += str(name) + " "
            text += "0 \n"
        f.write(text)
        f.close()

    def resolve(self):
        """
        Lance un ensemble de fonctions permettant de résoudre le norinori
        """
        self.__generateNeighborClauses()
        self.__generateZoneClauses()
        if self.gridLib.getNumberColoredCells() > 0:
            self.__filterClauses()
