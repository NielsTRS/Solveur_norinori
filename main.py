# coding : utf-8

import libs.rule as rule
import libs.grid as grid

n = 2
zone = 1

grille = grid.Grid(n, zone)
regle = rule.Rule(n)

print(grille.getGrid())

grille.setCellValueColor(1, 1, 1)

regle.generateClauses(grille)
print(regle.getClauses())

regle.filterClauses(grille)
print(regle.getClauses())

regle.generateDimacs("dimacs.txt")