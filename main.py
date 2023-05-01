# coding : utf-8

import timeit
import libs.rule as rule
import libs.grid as grid
from pysat.solvers import Glucose3
from pysat.formula import CNF


def start():
    starttime = timeit.default_timer()

    n = 5  #taille de la grille
    zone = 6  # nombre de zones
    name = "dimacs.cnf" #fichier dimacs qui sera généré

    grille = grid.Grid(n, zone)
    regle = rule.Rule(grille)

    # Zone configuration

    grille.setCellValueZone(2, 2, 1)
    grille.setCellValueZone(3, 1, 1)
    grille.setCellValueZone(3, 2, 1)
    grille.setCellValueZone(3, 3, 1)
    grille.setCellValueZone(4, 2, 1)
    grille.setCellValueZone(4, 3, 1)


    grille.setCellValueZone(1, 1, 2)
    grille.setCellValueZone(1, 2, 2)
    grille.setCellValueZone(2, 1, 2)

    grille.setCellValueZone(1, 3, 3)
    grille.setCellValueZone(1, 4, 3)
    grille.setCellValueZone(2, 3, 3)
    grille.setCellValueZone(2, 4, 3)

    grille.setCellValueZone(1, 5, 4)
    grille.setCellValueZone(2, 5, 4)
    grille.setCellValueZone(3, 5, 4)
    grille.setCellValueZone(4, 5, 4)

    grille.setCellValueZone(3, 4, 5)
    grille.setCellValueZone(4, 4, 5)
    grille.setCellValueZone(5, 4, 5)
    grille.setCellValueZone(5, 5, 5)

    grille.setCellValueZone(4, 1, 6)
    grille.setCellValueZone(5, 1, 6)
    grille.setCellValueZone(5, 2, 6)
    grille.setCellValueZone(5, 3, 6)

    # Résolution
    regle.resolve()

    regle.generateDimacs(name)


    print("Time clauses generation :", timeit.default_timer() - starttime)


    # sat solver
    cnf = CNF(from_file=name)  # reading from file

    solver = Glucose3()

    # Add the clauses to the solver
    solver.append_formula(cnf)

    # Solve the SAT problem
    solution = solver.solve()

    # Print the solution
    if solution:
        model = solver.get_model()
        print('Satisfiable')
        cells = []
        for idCell in model:
            if 0 < idCell < n * n + 1:
                cells.append(idCell)
                print(f"Il faut colorier la case de coordonnées : {grille.getCellIJById(idCell)}")
        if len(cells) == 0:
            print('Non satisfiable')
    else:
        print('Non satisfiable')

    print("Total time : ", timeit.default_timer() - starttime)



start()
