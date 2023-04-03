from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import libs.rule as rule
import libs.grid as grid
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


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=4000)
