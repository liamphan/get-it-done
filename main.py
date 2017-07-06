# Object relational mapping with Python, Flask, SQL, MySQLAlchemy

from flask import Flask, request, redirect, render_template
# importing sqlalchemy modules
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
# SQL database configurations. Server name:Server password:port/server name.
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://get-it-done:getitdone@localhost:8889/get-it-done'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

# persistent task class
class Task(db.Model):
    # every persistent class needs an id
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(120))
    completed = db.Column(db.Boolean)

    def __init__(self, name):
        self.name = name
        self.completed = False

# user class for login information
class User(db.Model):
    # three fields for the user object
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(120), unique = True)
    password = db.Column(db.String(120))

    # initializer or constructor for user class
    def __init__(self, email, password):
        self.email = email
        self.password = password

# login handlers
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email = email).first()
        if user and user.password == password:
            # TODO - "Remember" that the user has logged in.
            return redirect('/')
        else:
            # TODO - Explain why the login failed
            return '<h1>Error!</h1>'

    return render_template('login.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        verify = request.form['verify']

        # TODO - validate user's input data

        existing_user = User.query.filter_by(email = email).first()
        if not existing_user:
            new_user = User(email, password)
            db.session.add(new_user)
            db.session.commit()
            # TODO - "Remember" the user information
            return redirect('/')
        else:
            # TODO - user better response messaging
            return "<h1>Duplicate User</h1>"

    return render_template('register.html')

# index request handler
@app.route('/', methods=['POST', 'GET'])
def index():

    # if request is POST, coming from submitting the form.
    # then grab that data and creates a new class
    if request.method == 'POST':
        task_name = request.form['task']
        new_task = Task(task_name)
        db.session.add(new_task)
        db.session.commit()

    tasks = Task.query.filter_by(completed = False).all()
    completed_tasks = Task.query.filter_by(completed = True).all()
    return render_template('todos.html', title = "Get It Done!",
        tasks = tasks, completed_tasks = completed_tasks)

#  delete task request handler
@app.route('/delete-task', methods=['POST'])
def delete_task():

    task_id = int(request.form['task-id'])
    task = Task.query.get(task_id)
    task.completed = True
    db.session.add(task)
    db.session.commit()

    return redirect('/')

if __name__ == '__main__':
    app.run()
