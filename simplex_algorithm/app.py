from flask import Flask, render_template, request, json, url_for
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
    res = client.send(data)
    return_x = 'Solution vector: {}'.format(res['result_x'])
    return_ans = 'Optimal value: {}'.format(res['result_ans'])
    return_iter = 'Reached in {} iterations'.format(res['result_iter'])
    return_id = int(res['result_id'])
    link = url_for('show_data', identifier=return_id, _external=True)
    return render_template('index.html', result_x=return_x, result_ans=return_ans, result_iter=return_iter,
                           m_A=_matrix, v_b=_vector_b, v_c=_vector_c, link=link)


@app.route("/<identifier>", methods=['POST', 'GET'])
def show_data(identifier):
    data = str(identifier)
    # data = json.dumps(data)
    res = client.send_to_show(data)
    return render_template('show_data.html', matrix=res['matrix'], b_vector=res['b_vector'],
                           c_vector=res['c_vector'], opt_val=res['opt_val'], x_vector=res['x_vector'])


if __name__ == "__main__":
    app.run()
    client.close()
