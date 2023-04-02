# coding : utf-8

import libs.rule as rule
import libs.grid as grid

n = 2
zone = 1

grille = grid.Grid(n, zone)
regle = rule.Rule(n)

grille.setCellValueColor(1, 1, 1)

print(grille.getGrid())
regle.generateClauses()
print(regle.getClauses())
print(regle.getClauses())

regle.generateDimacs("dimacs.txt")