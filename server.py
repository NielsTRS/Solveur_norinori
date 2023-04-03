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
    zone = 2
    grille = grid.Grid(n, zone)
    regle = rule.Rule(n)
    grilleGen = grille.getGrid()
    cells = {
        'cells': grilleGen
    }
    return jsonify(cells)

@app.route('/solveGrid', methods=['POST'])
def solveGrid():
    data = request.get_json()
    n = int(data["gridSize"])
    zone = 1
    grille = grid.Grid(n, zone)
    regle = rule.Rule(n)
    cellsToColor = data["cellsToColor"]
    for cell in cellsToColor:
        grille.setCellValueColor(cell[0]+1, cell[1]+1, 1)
    regle.generateClauses(grille)
    regle.filterClauses(grille)
    regle.generateDimacs("dimacs.cnf")
    cnf = CNF(from_file="dimacs.cnf")  # reading from file
    solver = Lingeling()
    solver.append_formula(cnf)
    solution = solver.solve()
    if solution:
        model = solver.get_model()
        cellsToUpdate = []
        for id in model:
            if id > 0:
                cellsToUpdate.append(grille.getCellIJById(id))
        return jsonify({'solution': cellsToUpdate})
    else:
        return jsonify({'error': True})



if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=4000)
