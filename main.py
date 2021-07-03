from flask import Flask, request
from flask import render_template
from flask import redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder='template')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
db.create_all()


#Create the database to fill the columns with the information given by the user
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100))
    done = db.Column(db.Boolean)


@app.route('/')
def tasks_list():
    tasks = Task.query.all()
    return render_template('list.html', tasks=tasks)


#Create the addition of a new task in the DB
@app.route('/task', methods=['POST'])
def add_task():
    content = request.form['content']
    new_task = Task(content=content, done=False)
    db.session.add(new_task)
    db.session.commit()
    return redirect('/')


#Delete information in the DB
@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    task = Task.query.filter_by(id=task_id).first()
    db.session.delete(task)
    db.session.commit()
    return redirect('/')


#Update a task in the DB
@app.route('/done/<int:task_id>')
def update_task(task_id):
    task = Task.query.filter_by(id=task_id).first()
    task.done = not task.done
    db.session.commit()
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)