from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import libs.rule as rule
import libs.grid as grid
from pysat.solvers import Lingeling
from pysat.formula import CNF

app = Flask(__name__)
CORS(app)


@app.route('/generateGrid', methods=['POST'])
def generateGrid():
    data = request.get_json()
    n = int(data["gridSize"])
    zone = 1
    grille = grid.Grid(n, zone)
    cells = {
        'cells': grille.getGrid()
    }
    return jsonify(cells)


@app.route('/solveGrid', methods=['POST'])
def solveGrid():
    name = "dimacs.cnf"
    data = request.get_json()
    n = int(data["gridSize"])
    zone = int(data["amountAreas"])
    grille = grid.Grid(n, zone)
    regle = rule.Rule(grille)
    cellsToColor = data["cellsToColor"]
    for cell in cellsToColor:
        grille.setCellValueColor(cell[0] + 1, cell[1] + 1, 1)
    cellsAreas = data["cellsAreas"]
    for area in cellsAreas:
        for cell in cellsAreas[area]:
            grille.setCellValueZone(cell[0] + 1, cell[1] + 1, int(area))
    regle.resolve()
    regle.generateDimacs(name)
    cnf = CNF(from_file=name)  # reading from file
    solver = Lingeling()
    solver.append_formula(cnf)
    solution = solver.solve()
    if solution:
        model = solver.get_model()
        print(model)
        cellsToUpdate = []
        for id in model:
            if 0 < id < n * n + 1:
                cellsToUpdate.append(grille.getCellIJById(id))
        if len(cellsToUpdate) > 1:
            return jsonify({'solution': cellsToUpdate})
        else:
            return jsonify({'error': True})
    else:
        return jsonify({'error': True})


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=4000)
