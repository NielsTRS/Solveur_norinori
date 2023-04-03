# coding : utf-8

import libs.rule as rule
import libs.grid as grid

n = 2
zone = 1

grille = grid.Grid(n, zone)
regle = rule.Rule(n)

grille.setCellValueColor(2, 2, 1)

regle.generateClauses()
print(regle.getClauses())

regle.filterClauses(grille)
print(regle.getClauses())

regle.generateDimacs("dimacs.txt")