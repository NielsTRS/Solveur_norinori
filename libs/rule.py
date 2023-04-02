# coding : utf-8

class Rule:
    def __init__(self, n: int):
        if not (isinstance(n, int)):
            raise TypeError("n doit être un entier")
        self.clauses = []
        self.nbVar = n * n
        self.n = n

    def generateClauses(self):
        for i in range(self.n):
            for j in range(self.n):
                if i == 0 and j == 0:  # case en haut a gauche x_{i-1,j} et x_{i,j-1} n'existent pas
                    self.clauses.append([f"-{i}{j}", f"{i}{j + 1}", f"{i + 1}{j}"])
                    self.clauses.append([f"-{i}{j}", f"-{i}{j + 1}", f"-{i + 1}{j}"])

                elif i == 0 and j == self.n - 1:  # case en haut à droite x_{i-1,j} et x_{i,j+1} n'existent pas
                    self.clauses.append([f"-{i}{j}", f"{i}{j - 1}", f"{i + 1}{j}"])
                    self.clauses.append([f"-{i}{j}", f"-{i}{j - 1}", f"-{i + 1}{j}"])

                elif i == self.n - 1 and j == 0:  # case en bas a gauche x_{i+1,j} et x_{i,j-1} n'existent pas
                    self.clauses.append([f"-{i}{j}", f"{i}{j + 1}", f"{i - 1}{j}"])
                    self.clauses.append([f"-{i}{j}", f"-{i}{j + 1}", f"-{i - 1}{j}"])

                elif i == self.n - 1 and j == self.n - 1:  # case en bas à droite x_{i+1,j} et x_{i,j+1} n'existent pas
                    self.clauses.append([f"-{i}{j}", f"{i}{j - 1}", f"{i - 1}{j}"])
                    self.clauses.append([f"-{i}{j}", f"-{i}{j - 1}", f"-{i - 1}{j}"])

                elif i == 0:  # cases sur la premiere ligne x_{i-1,j} n'existe pas
                    self.clauses.append([f"-{i}{j}", f"{i}{j - 1}", f"{i}{j + 1}", f"{i + 1}{j}"])
                    self.clauses.append([f"-{i}{j}", f"-{i}{j - 1}", f"-{i}{j + 1}"])
                    self.clauses.append([f"-{i}{j}", f"-{i}{j - 1}", f"-{i + 1}{j}"])
                    self.clauses.append([f"-{i}{j}", f"-{i}{j + 1}", f"-{i + 1}{j}"])

                elif i == self.n - 1:  # cases sur la derniere ligne x_{i+1,j} n'existe pas
                    self.clauses.append([f"-{i}{j}", f"{i}{j - 1}", f"{i}{j + 1}", f"{i - 1}{j}"])
                    self.clauses.append([f"-{i}{j}", f"-{i}{j - 1}", f"-{i}{j + 1}"])
                    self.clauses.append([f"-{i}{j}", f"-{i}{j - 1}", f"-{i - 1}{j}"])
                    self.clauses.append([f"-{i}{j}", f"-{i}{j + 1}", f"-{i - 1}{j}"])

                elif j == 0:  # cases sur la premiere colonne x_{i, j_1} n'existe pas
                    print("\n7")
                    self.clauses.append([f"-{i}{j}", f"{i + 1}{j}", f"{i}{j + 1}", f"{i - 1}{j}"])
                    self.clauses.append([f"-{i}{j}", f"-{i + 1}{j}", f"-{i}{j + 1}"])
                    self.clauses.append([f"-{i}{j}", f"-{i + 1}{j}", f"-{i - 1}{j}"])
                    self.clauses.append([f"-{i}{j}", f"-{i}{j + 1}", f"-{i - 1}{j}"])

                elif j == self.n - 1:  # cases sur la dernière colonne x_{i, j+1} n'existe pas
                    self.clauses.append([f"-{i}{j}", f"{i + 1}{j}", f"{i}{j - 1}", f"{i - 1}{j}"])
                    self.clauses.append([f"-{i}{j}", f"-{i + 1}{j}", f"-{i}{j - 1}"])
                    self.clauses.append([f"-{i}{j}", f"-{i + 1}{j}", f"-{i - 1}{j}"])
                    self.clauses.append([f"-{i}{j}", f"-{i}{j - 1}", f"-{i - 1}{j}"])

                else:  # toutes les autres cases
                    self.clauses.append([f"-{i}{j}", f"-{i - 1}{j}", f"-{i}{j - 1}"])
                    self.clauses.append([f"-{i}{j}", f"-{i - 1}{j}", f"-{i}{j + 1}"])
                    self.clauses.append([f"-{i}{j}", f"-{i - 1}{j}", f"-{i + 1}{j}"])
                    self.clauses.append([f"-{i}{j}", f"{i - 1}{j}", f"{i}{j - 1}", f"{i}{j + 1}", f"{i + 1}{j}"])
                    self.clauses.append([f"-{i}{j}", f"-{i}{j - 1}", f"-{i}{j + 1}"])
                    self.clauses.append([f"-{i}{j}", f"-{i}{j - 1}", f"-{i + 1}{j}"])
                    self.clauses.append([f"-{i}{j}", f"-{i}{j + 1}", f"-{i + 1}{j}"])
        return self

    def getClauses(self):
        return self.clauses

    def getNumberVar(self):
        return self.nbVar
