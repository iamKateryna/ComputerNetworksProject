from flask import Flask, render_template, request, json
import client

app = Flask(__name__)


@app.route("/")
def main():
    return render_template('index.html')


@app.route("/", methods=['POST'])
def get_data():
    _matrix = request.form['matrix']
    _vector_b = request.form['vector_b']
    _vector_c = request.form['vector_c']

    data = {'matrix': _matrix,
         'vector_b': _vector_b,
         'vector_c': _vector_c}

    data = json.dumps(data)
    client.send(data)
    return render_template('index.html')


if __name__ == "__main__":
    app.run()