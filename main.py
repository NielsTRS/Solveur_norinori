# coding : utf-8

import timeit
import libs.rule as rule
import libs.grid as grid
from pysat.solvers import Glucose3
from pysat.formula import CNF


def start():
    n = 3
    zone = 2
    name = "dimacs.cnf"

    grille = grid.Grid(n, zone)
    regle = rule.Rule(n, grille)

    grille.setCellValueZone(1, 1, 2)
    grille.setCellValueZone(1, 2, 2)

    # print(grille.getGrid())

    regle.resolve()

    #print(regle.getClauses())

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
        for idCell in model:
            if idCell > 0:
                print(f"Il faut colorier la case de coordonnées : {grille.getCellIJById(idCell)}")
    else:
        print('Non satisfiable')


# starttime = timeit.default_timer()
# print("The start time is :", starttime)
start()
# print("The time difference is :", timeit.default_timer() - starttime)