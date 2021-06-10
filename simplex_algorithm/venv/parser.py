import json
import numpy as np

def parse_json(data):
    dictionary = json.loads(data)

    matrix = dictionary['matrix']
    vector_b = dictionary['vector_b']
    vector_c = dictionary['vector_c']

    output_matrix = []
    for row in matrix.split(','):
        _row = []
        for number in row.split(' '):
            _row.append(float(number))
        output_matrix.append(_row)

    output_vector_b = []
    for number in vector_b.split(' '):
        output_vector_b.append(float(number))

    output_vector_c = []
    for number in vector_c.split(' '):
        output_vector_c.append(float(number))

    return np.array(output_matrix), np.array(output_vector_b), np.array(output_vector_c)

