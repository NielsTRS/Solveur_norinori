# coding : utf-8

import libs.rule as rule
import libs.grid as grid

n = 2
zone = 1

grille = grid.Grid(n, zone)
regle = rule.Rule(n)

print(grille.getGrid())
regle.generateClauses()
print(regle.getClauses())
print(regle.getNumberVar())

