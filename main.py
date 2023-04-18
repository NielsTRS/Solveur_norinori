# coding : utf-8

import timeit
import libs.rule as rule
import libs.grid as grid
from pysat.solvers import Glucose3
from pysat.formula import CNF


def start():
    n = 10
    zone = 2
    name = "dimacs.cnf"

    grille = grid.Grid(n, zone)
    regle = rule.Rule(grille)

    # Zone configuration
    grille.setCellValueZone(1, 1, 2)
    grille.setCellValueZone(1, 2, 2)

    # grille.setCellValueZone(5, 1, 3)
    # grille.setCellValueZone(5, 2, 3)

    # Optional color configuration to add difficulty
    grille.setCellValueColor(3, 3, grille.CELL_COLORED)

    # grille.setCellValueColor(5, 1, grille.CELL_COLORED)

    # print(grille.getGrid())

    regle.resolve()

    # print(regle.getClauses())

    regle.generateDimacs(name)

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


starttime = timeit.default_timer()
print("The start time is :", starttime)
start()
print("The time difference is :", timeit.default_timer() - starttime)
