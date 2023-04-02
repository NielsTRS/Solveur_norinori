# coding : utf-8

import libs.rule as rule
import libs.grid as grid

grille = grid.Grid(3, 2)

print(grille.getGrid())
grille.setCellValueZone(2, 2, 1)
print(grille.getGrid())

grille.setCellValueColor(2, 2, grille.CELL_COLORED)
print(grille.getGrid())
print(grille.getCellValue(2, 2, 1))