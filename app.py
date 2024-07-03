from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'  # SQLite database file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define Student model
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    dob = db.Column(db.Date, nullable=False)
    amount_due = db.Column(db.Float, nullable=False)

@app.route('/')
def index():
    return render_template('index.html') 


@app.route('/added', methods=['POST'])
def added():
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    dob = request.form.get('dob')
    amount_due = request.form.get('amount_due')

    # Create a new Student object
    new_student = Student(first_name=first_name,
                          last_name=last_name,
                          dob=dob,
                          amount_due=amount_due)

    # Add the new student to the database session
    db.session.add(new_student)
    db.session.commit()

    return redirect(url_for('list'))  # Redirect to the form page after submission

@app.route('/list')
def student_list():
    students = Student.query.all()
    return render_template('studentList.html', students=students)

if __name__ == '__main__':
    app.run(debug=True)