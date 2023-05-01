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
        self.vars = self.n * self.n - self.gridLib.getNumberColoredCells()

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
            casesInZone = self.gridLib.getCellsInZone(gridSize, k)
            
            n = len(casesInZone)
            if n < 1:
                raise AssertionError(f"Aucune case dans la zone {k}")
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
        colored = self.gridLib.CELL_COLORED
        for clause in clauses:
            filtered_clause = []
            add_clause = True
            for idCell in clause:
                coor = self.gridLib.getCellIJById(abs(idCell))
                color = self.gridLib.getCellValueColor(coor[0], coor[1])
                if color != colored:
                    filtered_clause.append(idCell)
                else:
                    if idCell > 0:
                        add_clause = False
                        break  # on évite de boucler sur les autres terms alors qu'on ne pas garder la clause
            if add_clause:
                filtered_clauses.append(filtered_clause)

        self.clauses = filtered_clauses

    def __getNumberVar(self):
        """
        Renvoie le nombre d'identifiants différents dans les clauses
        :return: nombre identifiant
        :rtype: int
        """
        return self.vars

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

    def threeSatFormat(self):
        """
        Permet de transformer les clauses de n-sat en 3-sat
        """
        maxvar = self.vars
        clauses = self.getClauses()
        new_clauses = []
        for clause in clauses:
            size = len(clause)
            if size > 3:
                maxvar += 1  # variable supplémentaire
                new_clauses.append([clause[0], clause[1], maxvar])
                for i in range(2, size - 2):
                    new_clause = []
                    new_clause.append(-maxvar)
                    new_clause.append(clause[i])
                    maxvar += 1
                    new_clause.append(maxvar)
                    new_clauses.append(new_clause)
                new_clauses.append([-maxvar, clause[size - 2], clause[size - 1]])
            elif size == 2:
                maxvar += 1  # variable supplémentaire
                new_clauses.append([clause[0], clause[1], maxvar])
                new_clauses.append([clause[0], clause[1], -maxvar])
            elif size == 1:
                maxvar += 2
                y = maxvar - 1  # variable supplémentaire 1
                z = maxvar  # variable supplémentaire 2
                new_clauses.append([clause[0], y, z])
                new_clauses.append([clause[0], y, -z])
                new_clauses.append([clause[0], -y, z])
                new_clauses.append([clause[0], -y, -z])
            else:
                new_clauses.append(clause)
        self.clauses = new_clauses
        self.vars = maxvar

    def resolve(self):
        """
        Lance un ensemble de fonctions permettant de résoudre le norinori
        """
        self.__generateNeighborClauses()
        self.__generateZoneClauses()
        if self.gridLib.getNumberColoredCells() > 0:
            self.__filterClauses()
        self.threeSatFormat()
