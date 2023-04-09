# coding : utf-8

import itertools

import libs.grid as grid


class Rule:
    def __init__(self, n: int, gridLib: grid):
        if not (isinstance(n, int)):
            raise TypeError("n doit être un entier")
        self.clauses = []
        self.n = n
        self.gridLib = gridLib

    def __generateNeighborClauses(self):
        def addClause(x, y, positive, *args):
            tempClauses = []
            add = True
            prefix = "" if positive else "-"
            tempClauses.append(int(f"{prefix}{self.gridLib.getIdCell(x, y)}"))
            for arg in args:
                prefix = "" if arg[2] else "-"
                tempClauses.append(int(f"{prefix}{self.gridLib.getIdCell(arg[0], arg[1])}"))
            if add:
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

        return self

    def __generateZoneClauses(self):
        gridSize = self.gridLib.getGridSize()
        gridZoneNumber = self.gridLib.getZoneNumber()
        for k in range(1, gridZoneNumber + 1):
            casesInZone = []
            for i in range(1, gridSize + 1):
                for j in range(1, gridSize + 1):
                    if self.gridLib.getCellValueZone(i, j) == k:
                        casesInZone.append(self.gridLib.getIdCell(i, j))
            n = len(casesInZone)
            print(f"{n} cases de la zone {k} :  {casesInZone}")
            combs = itertools.combinations(range(1, n + 1), n - 1)
            for comb in combs:
                temp = []
                for j in comb:
                    temp.append(int(f"{casesInZone[j - 1]}"))
                self.clauses.append(temp)

            combs = itertools.combinations(range(1, n + 1), 3)
            for comb in combs:
                temp = []
                for j in comb:
                    temp.append(int(f"-{casesInZone[j - 1]}"))
                self.clauses.append(temp)
        print(self.getClauses())

    def __filterClauses(self):
        clauses = self.getClauses()
        filtered_clauses = []
        for clause in clauses:
            filtered_clause = []
            add_clause = True
            for name in clause:
                cell = self.gridLib.getCellIJById(abs(name))
                color = self.gridLib.getCellValueColor(cell[0], cell[1])
                if not str(name)[0] == "-":
                    if color != self.gridLib.CELL_COLORED:
                        filtered_clause.append(name)
                    else:
                        add_clause = False
                        break  # on évite de boucler sur les autres terms alors qu'on ne pas garder la clause
                else:
                    if color != self.gridLib.CELL_COLORED:
                        filtered_clause.append(name)
            if add_clause:
                filtered_clauses.append(filtered_clause)

        self.clauses = filtered_clauses
        return self

    def __getNumberVar(self):
        return self.n * self.n

    def __getNumberClauses(self):
        return len(self.getClauses())

    def getClauses(self):
        return self.clauses

    def generateDimacs(self, filename):
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
        self.__generateNeighborClauses()
        self.__generateZoneClauses()
        self.__filterClauses()

