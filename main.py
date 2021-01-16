import csv

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

database = SQLAlchemy()
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cst-database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

class student(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    name = database.Column(database.String(100), nullable=False)
    branch = database.Column(database.String(40), nullable=False)
    college = database.Column(database.String(60), nullable=False)
    batch = database.Column(database.String(30), nullable=False)
    program = database.Column(database.String(30), nullable=False)
    course = database.Column(database.String(40), nullable=False)
    first_lang = database.Column(database.String(60), nullable=False)

    def __init__(self, id, name, branch, college, batch, program, course, first_lang):
        self.id = id
        self.name = name
        self.branch = branch
        self.college = college
        self.batch = batch
        self.program = program
        self.course = course
        self.first_lang = first_lang

    def to_json(self):
        return {'ID': self.id, 'Name': self.name, 'Branch': self.branch, 'College': self.college, 'Batch': self.batch,
                'Program': self.program, 'Course': self.course, 'First Language': self.first_lang}

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def save(self):
        database.session.add(self)
        database.session.commit()


database.init_app(app)
app.app_context().push()
database.reflect()
database.drop_all()
database.create_all()

with open('records.csv') as data:
    all_records = csv.reader(data, delimiter=',')
    for record in all_records:
        stud = student(int(record[0]), record[1], record[2], record[3], record[4], record[5], record[6], record[7])
        stud.save()


@app.route('/mcit/cst-students/all')
def get_all_students():
    return {"All students" : list(map(lambda x: x.to_json(), student.query.all()))}


if __name__ == '__main__':
    app.run()
