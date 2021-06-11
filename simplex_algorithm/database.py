from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app_ = Flask(__name__)
app_.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://arsen:mypass10@localhost:5432/cm_project"
db = SQLAlchemy(app_)


class History(db.Model):
    __tablename__ = 'history'

    id = db.Column(db.Integer(), primary_key=True)
    matrix = db.Column(db.String(100))
    b_vector = db.Column(db.String(40))
    c_vector = db.Column(db.String(40))
    opt_val = db.Column(db.String(40))
    x_vector = db.Column(db.String(40))

    def __init__(self, matrix, b_vector, c_vector, opt_val, x_vector):
        self.matrix = matrix
        self.b_vector = b_vector
        self.c_vector = c_vector
        self.opt_val = opt_val
        self.x_vector = x_vector


if __name__ == '__main__':
    db.create_all()
