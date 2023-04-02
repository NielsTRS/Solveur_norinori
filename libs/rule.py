# coding : utf-8

class Rule:
    def __init__(self, n: int):
        if not (isinstance(n, int)):
            raise TypeError("n doit être un entier")
        self.clauses = []
        self.nbVar = n * n
        self.n = n

    def generateClauses(self):
        for i in range(1, self.n + 1):
            for j in range(1, self.n + 1):
                if i == 1 and j == 1:  # case en haut a gauche x_{i-1,j} et x_{i,j-1} n'existent pas
                    self.clauses.append([int(f"-{i}{j}"), int(f"{i}{j + 1}"), int(f"{i + 1}{j}")])
                    self.clauses.append([int(f"-{i}{j}"), int(f"-{i}{j + 1}"), int(f"-{i + 1}{j}")])

                elif i == 1 and j == self.n:  # case en haut à droite x_{i-1,j} et x_{i,j+1} n'existent pas
                    self.clauses.append([int(f"-{i}{j}"), int(f"{i}{j - 1}"), int(f"{i + 1}{j}")])
                    self.clauses.append([int(f"-{i}{j}"), int(f"-{i}{j - 1}"), int(f"-{i + 1}{j}")])

                elif i == self.n and j == 1:  # case en bas a gauche x_{i+1,j} et x_{i,j-1} n'existent pas
                    self.clauses.append([int(f"-{i}{j}"), int(f"{i}{j + 1}"), int(f"{i - 1}{j}")])
                    self.clauses.append([int(f"-{i}{j}"), int(f"-{i}{j + 1}"), int(f"-{i - 1}{j}")])

                elif i == self.n and j == self.n:  # case en bas à droite x_{i+1,j} et x_{i,j+1} n'existent pas
                    self.clauses.append([int(f"-{i}{j}"), int(f"{i}{j - 1}"), int(f"{i - 1}{j}")])
                    self.clauses.append([int(f"-{i}{j}"), int(f"-{i}{j - 1}"), int(f"-{i - 1}{j}")])

                elif i == 1:  # cases sur la premiere ligne x_{i-1,j} n'existe pas
                    self.clauses.append([int(f"-{i}{j}"), int(f"{i}{j - 1}"), int(f"{i}{j + 1}"), int(f"{i + 1}{j}")])
                    self.clauses.append([int(f"-{i}{j}"), int(f"-{i}{j - 1}"), int(f"-{i}{j + 1}")])
                    self.clauses.append([int(f"-{i}{j}"), int(f"-{i}{j - 1}"), int(f"-{i + 1}{j}")])
                    self.clauses.append([int(f"-{i}{j}"), int(f"-{i}{j + 1}"), int(f"-{i + 1}{j}")])

                elif i == self.n:  # cases sur la derniere ligne x_{i+1,j} n'existe pas
                    self.clauses.append([int(f"-{i}{j}"), int(f"{i}{j - 1}"), int(f"{i}{j + 1}"), int(f"{i - 1}{j}")])
                    self.clauses.append([int(f"-{i}{j}"), int(f"-{i}{j - 1}"), int(f"-{i}{j + 1}")])
                    self.clauses.append([int(f"-{i}{j}"), int(f"-{i}{j - 1}"), int(f"-{i - 1}{j}")])
                    self.clauses.append([int(f"-{i}{j}"), int(f"-{i}{j + 1}"), int(f"-{i - 1}{j}")])

                elif j == 1:  # cases sur la premiere colonne x_{i, j_1} n'existe pas
                    self.clauses.append([int(f"-{i}{j}"), int(f"{i + 1}{j}"), int(f"{i}{j + 1}"), int(f"{i - 1}{j}")])
                    self.clauses.append([int(f"-{i}{j}"), int(f"-{i + 1}{j}"), int(f"-{i}{j + 1}")])
                    self.clauses.append([int(f"-{i}{j}"), int(f"-{i + 1}{j}"), int(f"-{i - 1}{j}")])
                    self.clauses.append([int(f"-{i}{j}"), int(f"-{i}{j + 1}"), int(f"-{i - 1}{j}")])

                elif j == self.n:  # cases sur la dernière colonne x_{i, j+1} n'existe pas
                    self.clauses.append([int(f"-{i}{j}"), int(f"{i + 1}{j}"), int(f"{i}{j - 1}"), int(f"{i - 1}{j}")])
                    self.clauses.append([int(f"-{i}{j}"), int(f"-{i + 1}{j}"), int(f"-{i}{j - 1}")])
                    self.clauses.append([int(f"-{i}{j}"), int(f"-{i + 1}{j}"), int(f"-{i - 1}{j}")])
                    self.clauses.append([int(f"-{i}{j}"), int(f"-{i}{j - 1}"), int(f"-{i - 1}{j}")])

                else:  # toutes les autres cases
                    self.clauses.append([int(f"-{i}{j}"), int(f"-{i - 1}{j}"), int(f"-{i}{j - 1}")])
                    self.clauses.append([int(f"-{i}{j}"), int(f"-{i - 1}{j}"), int(f"-{i}{j + 1}")])
                    self.clauses.append([int(f"-{i}{j}"), int(f"-{i - 1}{j}"), int(f"-{i + 1}{j}")])
                    self.clauses.append([int(f"-{i}{j}"), int(f"{i - 1}{j}"), int(f"{i}{j - 1}"), int(f"{i}{j + 1}"),
                                         int(f"{i + 1}{j}")])
                    self.clauses.append([int(f"-{i}{j}"), int(f"-{i}{j - 1}"), int(f"-{i}{j + 1}")])
                    self.clauses.append([int(f"-{i}{j}"), int(f"-{i}{j - 1}"), int(f"-{i + 1}{j}")])
                    self.clauses.append([int(f"-{i}{j}"), int(f"-{i}{j + 1}"), int(f"-{i + 1}{j}")])
        return self

    def getClauses(self):
        return self.clauses

    def getNumberVar(self):
        return self.nbVar

    def getNumberClauses(self):
        return len(self.clauses)

    def generateDimacs(self, filename):
        f = open(filename, "w")
        f.write(f"p cnf {self.getNumberVar()} {self.getNumberClauses()} \n")
        text = ""
        for clause in self.getClauses():
            for name in clause:
                text += str(name) + " "
            text += "0 \n"
        f.write(text)
        f.close()
