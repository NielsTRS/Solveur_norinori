# coding : utf-8

import libs.rule as rule
import libs.grid as grid
from pysat.solvers import Glucose3
from pysat.formula import CNF

n = 2
zone = 1
name = "dimacs.cnf"

grille = grid.Grid(n, zone)
regle = rule.Rule(n)

print(grille.getGrid())

grille.setCellValueColor(1, 1, 1)

regle.generateClauses(grille)
print(regle.getClauses())

regle.filterClauses(grille)
print(regle.getClauses())

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
    print('Solution:', model)
    for idCell in model:
        if idCell > 0:
            print(f"Il faut colorier la case de coordonnées : {grille.getCellIJById(idCell)}")
else:
    print('Non satisfiable')
